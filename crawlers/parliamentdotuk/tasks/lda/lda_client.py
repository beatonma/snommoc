import time
from typing import (
    Dict,
    Optional,
    Callable,
    List,
    Tuple,
)

import logging
import requests
from django.conf import settings

from crawlers.parliamentdotuk.tasks.lda.endpoints import (
    MAX_PAGE_SIZE,
    PARAM_PAGE_SIZE,
    PARAM_PAGE,
)
from notifications.models import TaskNotification

log = logging.getLogger(__name__)


def get_next_page_url(json_response) -> Optional[str]:
    try:
        return json_response.get('result').get("next")
    except AttributeError as e:
        log.warning(e)
        return None


def get_value(data: Dict, key: str) -> Optional[str]:
    """LDA data values are often but not always wrapped in a structure like
    {'label': { '_value': 'actual value' } }"""
    v = data.get(key)
    if isinstance(v, str):
        return v
    elif isinstance(v, Dict):
        if '_value' in v.keys():
            return v.get('_value')
        elif 'label' in v.keys():
            try:
                return v.get('label').get('_value')
            except AttributeError:
                return None


def get_page(
        endpoint: str,
        page_number: int = 0,
        page_size: int = MAX_PAGE_SIZE,
) -> requests.Response:
    log.debug(endpoint)
    response = requests.get(
        endpoint,
        headers=settings.HTTP_REQUEST_HEADERS,
        params={
            PARAM_PAGE_SIZE: page_size,
            PARAM_PAGE: page_number,
        })

    return response


def update_model(
        endpoint_url: str,
        update_item_func: Callable[[Dict], Optional[str]],
        report_func: Optional[Callable[[List[str]], Tuple[str, str]]],
        page_size=MAX_PAGE_SIZE,
        page_load_delay: int = 5,  # Basic rate limiting
) -> None:
    new_items = []
    page_number = 0
    next_page = 'next-page-placeholder'

    TaskNotification.objects.create(
        title='Task started',
        content=f'An update cycle has started for endpoint {endpoint_url}'
    ).save()

    while next_page is not None:
        response = get_page(endpoint_url, page_number=page_number, page_size=page_size)

        if response.status_code != 200:
            log.warning(f'Failed to update: {response.url} [status={response.status_code}]')

        try:
            data = response.json()
            items = data.get('result').get('items')
        except AttributeError as e:
            log.warning(f'Could not read item list: {e}')
            return

        for item in items:
            new_name = update_item_func(item)
            if new_name:
                new_items.append(new_name)

        page_number += 1
        next_page = get_next_page_url(data)
        if next_page:
            time.sleep(page_load_delay)

    if report_func:
        title, content = report_func(new_items)
        TaskNotification.objects.create(
            title=title,
            content=content
        ).save()
