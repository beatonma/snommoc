from typing import (
    Dict,
    Optional,
)

import logging
import requests
from django.conf import settings

from crawlers.parliamentdotuk.tasks.lda.endpoints import (
    MAX_PAGE_SIZE,
    PARAM_PAGE_SIZE,
    PARAM_PAGE,
)


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
        page_size: int = MAX_PAGE_SIZE
) -> requests.Response:
    response = requests.get(
        endpoint,
        headers=settings.HTTP_REQUEST_HEADERS,
        params={
            PARAM_PAGE_SIZE: page_size,
            PARAM_PAGE: page_number,
        })

    return response
