import logging
from typing import Optional

from celery import shared_task

from crawlers.parliamentdotuk.tasks.lda import endpoints
from notifications.models import TaskNotification
from repository.models import Constituency
from .util import (
    get_value,
    get_page,
    get_next_page_url,
)

log = logging.getLogger(__name__)


@shared_task
def update_constituencies(report: bool = True) -> None:
    """
    :param report: Create a TaskNotification with the results of this task
    """
    def build_constituency(json_data) -> Optional[str]:
        if json_data.get('endedDate'):
            log.debug(f'Skipping obsolete constituency: {get_value(json_data, "label")}')
            return

        name = get_value(json_data, 'label')
        constituency, created = Constituency.objects.update_or_create(
            name=name,
            defaults={
                'name': name,
                'gss_code': get_value(json_data, 'gssCode'),
                'ordinance_survey_name': get_value(json_data, 'osName'),
                'constituency_type': get_value(json_data, 'constituencyType')
            }
        )
        constituency.save()

        if created:
            return name

    new_constituencies = []
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
            new_name = build_constituency(item)
            if new_name:
                new_constituencies.append(new_name)

        page_number += 1
        next_page = get_next_page_url(data)

    if report:
        title = 'Constituencies updated'
        if new_constituencies:
            constituency_list_text = '\n  '.join(new_constituencies)
            content = f'{len(new_constituencies)} new constituencies:\n{constituency_list_text}'
        else:
            content = 'No new constituencies'

        TaskNotification.objects.create(
            title=title,
            content=content
        ).save()
