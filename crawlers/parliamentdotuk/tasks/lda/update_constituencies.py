import logging
from celery import shared_task

from crawlers.parliamentdotuk.tasks.lda import endpoints
from repository.models import Constituency
from .util import (
    get_value,
    get_page,
    get_next_page_url,
)

log = logging.getLogger(__name__)


@shared_task
def update_constituencies():
    def build_constituency(json_data):
        if json_data.get('endedDate'):
            log.debug(f'Skipping obsolete constituency: {get_value(json_data, "label")}')
            return

        constituency, _ = Constituency.objects.update_or_create(
            name=get_value(json_data, 'label'),
            defaults={
                'gss_code': get_value(json_data, 'gssCode'),
                'ordinance_survey_name': get_value(json_data, 'osName'),
                'constituency_type': get_value(json_data, 'constituencyType')
            }
        )
        print(constituency)
        constituency.save()

    page_number = 0
    next_page = 'next-page-placeholder'
    while next_page is not None:
        response = get_page(endpoints.CONSTITUENCIES_BASE_URL, page_number=page_number)

        if response.status_code != 200:
            log.warning(
                f'Failed to update constituencies: {response.url} '
                f'returned status={response.status_code}')
            return

        try:
            data = response.json()
            items = data.get('result').get('items')
        except AttributeError as e:
            log.warning(f'Could not read constituency list: {e}')
            return

        for item in items:
            build_constituency(item)

        page_number += 1
        next_page = get_next_page_url(data)

