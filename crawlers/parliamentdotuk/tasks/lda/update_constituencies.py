import logging

from celery import shared_task

from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import (
    constituencies as constituencies_contract,
)
from notifications.models.task_notification import task_notification
from repository.models import Constituency
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_parliamentdotuk_id,
    get_str,
    update_model,
    get_date,
)
from crawlers.parliamentdotuk.tasks.network import json_cache

log = logging.getLogger(__name__)


@shared_task
@task_notification(label="Update constituencies")
@json_cache(name="constituencies")
def update_constituencies(follow_pagination=True, **kwargs) -> None:
    def build_constituency(json_data):
        puk = get_parliamentdotuk_id(json_data)
        name = get_str(json_data, constituencies_contract.NAME)

        Constituency.objects.update_or_create(
            parliamentdotuk=puk,
            defaults={
                "name": name,
                "gss_code": get_str(json_data, constituencies_contract.GSS_CODE),
                "ordinance_survey_name": get_str(
                    json_data,
                    constituencies_contract.ORDINANCE_SURVEY_NAME,
                    default="",
                ),
                "constituency_type": get_str(json_data, constituencies_contract.TYPE),
                "start": get_date(json_data, constituencies_contract.DATE_STARTED),
                "end": get_date(json_data, constituencies_contract.DATE_ENDED),
            },
        )

    update_model(
        endpoints.CONSTITUENCIES_BASE_URL,
        update_item_func=build_constituency,
        follow_pagination=follow_pagination,
        **kwargs,
    )
