import logging
from typing import Optional

from crawlers import caches
from crawlers.network import JsonResponseCache, json_cache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from notifications.models import TaskNotification
from notifications.models.task_notification import task_notification
from repository.models import House
from repository.models.bill import BillStageType

log = logging.getLogger(__name__)


def _update_bill_stage_type(
    data: dict,
    notification: Optional[TaskNotification],
) -> None:
    """Signature: openapi_client.ItemFunc"""
    stage = schema.BillStageType(**data)
    house, _ = House.objects.get_or_create(name=stage.house.name)

    BillStageType.objects.update_or_create(
        parliamentdotuk=stage.id,
        defaults={
            "name": stage.name,
            "house": house,
        },
    )


@task_notification(label="Update bill stage types")
@json_cache(caches.BILLS)
def update_bill_stage_types(
    cache: Optional[JsonResponseCache],
    notification: Optional[TaskNotification],
):
    log.info("Updating BillStageTypes...")
    openapi_client.foreach(
        endpoints.BILL_STAGE_DEFINITIONS,
        item_func=_update_bill_stage_type,
        cache=cache,
        notification=notification,
    )
    log.info("BillStageTypes updated successfully")
