import logging
from typing import Optional

from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.network import JsonCache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from notifications.models import TaskNotification
from repository.models import House
from repository.models.bill import BillStageType

log = logging.getLogger(__name__)


def _update_bill_stage_type(data: dict, context: TaskContext) -> None:
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


@task_context(cache_name=caches.BILLS, label="Update bill stage types")
def update_bill_stage_types(
    cache: Optional[JsonCache],
    notification: Optional[TaskNotification],
):
    context = TaskContext(cache, notification)
    log.info("Updating BillStageTypes...")
    openapi_client.foreach(
        endpoints.BILL_STAGE_DEFINITIONS,
        item_func=_update_bill_stage_type,
        context=context,
    )
    log.info("BillStageTypes updated successfully")
