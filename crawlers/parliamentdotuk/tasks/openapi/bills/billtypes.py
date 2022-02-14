from typing import Optional

from crawlers.network import JsonResponseCache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import viewmodels
from notifications.models import TaskNotification
from repository.models.bill import BillType, BillTypeCategory


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


def update_bill_types(
    cache: Optional[JsonResponseCache],
    notification: Optional[TaskNotification],
) -> None:
    openapi_client.foreach(
        endpoint_url=endpoints.BILL_TYPE_DEFINITIONS,
        item_func=_update_bill_type,
        notification=notification,
        cache=cache,
    )
