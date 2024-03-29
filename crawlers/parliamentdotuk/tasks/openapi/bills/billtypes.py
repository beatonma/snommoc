import logging
from typing import Optional

from crawlers import caches
from crawlers.network import JsonResponseCache, json_cache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import viewmodels
from notifications.models import TaskNotification
from notifications.models.task_notification import task_notification
from repository.models.bill import BillType, BillTypeCategory

log = logging.getLogger(__name__)


def _update_bill_type(
    data: dict,
    notification: Optional[TaskNotification],
) -> None:
    billtype = viewmodels.BillType(**data)

    category, _ = BillTypeCategory.objects.get_or_create(name=billtype.category.name)

    BillType.objects.update_or_create(
        parliamentdotuk=billtype.id,
        defaults={
            "name": billtype.name,
            "description": billtype.description,
            "category": category,
        },
    )


@task_notification(label="Update bill types")
@json_cache(caches.BILLS)
def update_bill_types(
    cache: Optional[JsonResponseCache],
    notification: Optional[TaskNotification],
) -> None:
    log.info("Updating BillTypes...")
    openapi_client.foreach(
        endpoint_url=endpoints.BILL_TYPE_DEFINITIONS,
        item_func=_update_bill_type,
        notification=notification,
        cache=cache,
    )
    log.info("BillTypes updated successfully")
