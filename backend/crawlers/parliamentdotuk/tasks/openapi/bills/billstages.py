from typing import Optional

from crawlers.network import JsonResponseCache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills.viewmodels import StageSummary
from notifications.models import TaskNotification
from repository.models import House, ParliamentarySession
from repository.models.bill import BillStage, BillStageSitting


def _update_bill_stage(
    data: dict, notification: Optional[TaskNotification], func_kwargs: dict
):
    """Signature: openapi_client.ItemFunc"""
    api_stage = StageSummary(**data)
    bill_id = func_kwargs["bill_id"]

    session, _ = ParliamentarySession.objects.update_or_create(
        parliamentdotuk=api_stage.sessionId
    )
    house, _ = House.objects.get_or_create(name=api_stage.house.name)

    stage, _ = BillStage.objects.update_or_create(
        parliamentdotuk=api_stage.id,
        defaults={
            "bill_id": bill_id,
            "description": api_stage.description,
            "abbreviation": api_stage.abbreviation,
            "house": house,
            "session": session,
            "sort_order": api_stage.sortOrder,
            "stage_type_id": api_stage.stageId,
        },
    )

    for sitting in api_stage.stageSittings:
        BillStageSitting.objects.update_or_create(
            parliamentdotuk=sitting.id,
            stage_id=api_stage.id,
            date=sitting.date,
        )


def fetch_and_update_bill_stages(
    bill_id: int,
    cache: Optional[JsonResponseCache],
    notification: Optional[TaskNotification],
) -> None:
    openapi_client.foreach(
        endpoints.bill_stages(bill_id),
        item_func=_update_bill_stage,
        cache=cache,
        notification=notification,
        func_kwargs={
            "bill_id": bill_id,
        },
    )
