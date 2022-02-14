from typing import Optional

from crawlers.network import JsonResponseCache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import viewmodels
from notifications.models import TaskNotification
from repository.models import House
from repository.models.bill import BillStageType


def _update_bill_stage_type(
    data: dict,
    notification: Optional[TaskNotification],
) -> None:
    print(data)
    stage = viewmodels.BillStage(**data)
    house, _ = House.objects.get_or_create(name=stage.house.name)

    BillStageType.objects.update_or_create(
        parliamentdotuk=stage.id,
        defaults={
            "name": stage.name,
            "house": house,
        },
    )


def update_bill_stage_types(
    cache: Optional[JsonResponseCache],
    notification: Optional[TaskNotification],
):
    openapi_client.foreach(
        endpoints.BILL_STAGE_DEFINITIONS,
        item_func=_update_bill_stage_type,
        cache=cache,
        notification=notification,
    )
