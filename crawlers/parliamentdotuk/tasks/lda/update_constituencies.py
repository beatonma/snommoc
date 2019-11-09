import logging
from typing import Optional

from celery import shared_task

from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import constituencies as constituencies_contract
from repository.models import Constituency
from .lda_client import (
    get_value,
    update_model,
)

log = logging.getLogger(__name__)


@shared_task
def update_constituencies() -> None:
    def build_constituency(json_data) -> Optional[str]:
        if json_data.get(constituencies_contract.DATE_ENDED):
            # log.debug(f'Skipping obsolete constituency: {get_value(json_data, "label")}')
            return

        name = get_value(json_data, constituencies_contract.NAME)
        constituency, created = Constituency.objects.update_or_create(
            name=name,
            defaults={
                'name': name,
                'gss_code': get_value(json_data, constituencies_contract.GSS_CODE),
                'ordinance_survey_name': get_value(json_data, constituencies_contract.ORDINANCE_SURVEY_NAME),
                'constituency_type': get_value(json_data, constituencies_contract.TYPE)
            }
        )
        constituency.save()

        if created:
            return name

    def build_report(new_constituencies):
        title = 'Constituencies updated'
        if new_constituencies:
            constituency_list_text = '\n  '.join(new_constituencies)
            content = f'{len(new_constituencies)} new constituencies:\n{constituency_list_text}'
        else:
            content = 'No new constituencies'
        return title, content

    update_model(
        endpoints.CONSTITUENCIES_BASE_URL,
        update_item_func=build_constituency,
        report_func=build_report)
