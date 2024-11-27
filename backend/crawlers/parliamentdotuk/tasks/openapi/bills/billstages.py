from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from crawlers.parliamentdotuk.tasks.openapi.bills.schema import StageSummary
from repository.models import (
    BillStage,
    BillStageSitting,
    BillStageType,
    House,
    ParliamentarySession,
)


def fetch_and_update_bill_stages(bill_id: int, context: TaskContext) -> None:
    openapi_client.foreach(
        endpoints.bill_stages(bill_id),
        item_func=_update_bill_stage,
        context=context,
        func_kwargs={
            "bill_id": bill_id,
        },
    )


def update_bill_stage_types(context: TaskContext):
    openapi_client.foreach(
        endpoints.BILL_STAGE_DEFINITIONS,
        item_func=_update_bill_stage_type,
        context=context,
    )
    context.info("BillStageTypes updated successfully")


def _update_bill_stage(response_data: dict, context: TaskContext, func_kwargs: dict):
    """Signature: openapi_client.ItemFunc"""
    data = StageSummary.model_validate(response_data)
    bill_id = func_kwargs["bill_id"]

    session, _ = ParliamentarySession.objects.update_or_create(
        parliamentdotuk=data.session_id
    )
    house, _ = House.objects.get_or_create(name=data.house.name)

    stage, _ = BillStage.objects.update_or_create(
        parliamentdotuk=data.id,
        defaults={
            "bill_id": bill_id,
            "description": data.description,
            "abbreviation": data.abbreviation,
            "house": house,
            "session": session,
            "sort_order": data.sort_order,
            "stage_type_id": data.stage_id,
        },
    )

    for sitting in data.stage_sittings:
        BillStageSitting.objects.update_or_create(
            parliamentdotuk=sitting.id,
            stage_id=data.id,
            date=sitting.date,
        )


def _update_bill_stage_type(response_data: dict, context: TaskContext) -> None:
    """Signature: openapi_client.ItemFunc"""
    data = schema.BillStageType.model_validate(response_data)
    house, _ = House.objects.get_or_create(name=data.house.name)

    BillStageType.objects.update_or_create(
        parliamentdotuk=data.id,
        defaults={
            "name": data.name,
            "house": house,
        },
    )
