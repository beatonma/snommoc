import logging
from typing import Optional

from celery import shared_task

from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import (
    constituencies as constituencies_contract,
)
from notifications.models.task_notification import task_notification
from repository.models import Constituency
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_value,
    update_model,
    get_date,
    get_parliamentdotuk_id,
)
from crawlers.parliamentdotuk.tasks.network import json_cache

log = logging.getLogger(__name__)


@shared_task
@task_notification(label="Update constituencies")
@json_cache(name="constituencies")
def update_constituencies(follow_pagination=True, **kwargs) -> None:
    def build_constituency(json_data) -> Optional[str]:
        puk = get_parliamentdotuk_id(
            get_value(json_data, constituencies_contract.ABOUT)
        )
        name = get_value(json_data, constituencies_contract.NAME)
        constituency, created = Constituency.objects.update_or_create(
            parliamentdotuk=puk,
            defaults={
                "name": name,
                "gss_code": get_value(json_data, constituencies_contract.GSS_CODE),
                "ordinance_survey_name": get_value(
                    json_data, constituencies_contract.ORDINANCE_SURVEY_NAME
                ),
                "constituency_type": get_value(json_data, constituencies_contract.TYPE),
                "start": get_date(json_data, constituencies_contract.DATE_STARTED),
                "end": get_date(json_data, constituencies_contract.DATE_ENDED),
            },
        )

        if created:
            return name

    update_model(
        endpoints.CONSTITUENCIES_BASE_URL,
        update_item_func=build_constituency,
        follow_pagination=follow_pagination,
        **kwargs,
    )
