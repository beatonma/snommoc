from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from repository.models.bill import BillType, BillTypeCategory


def update_bill_types(context: TaskContext) -> None:
    openapi_client.foreach(
        endpoint_url=endpoints.BILL_TYPE_DEFINITIONS,
        item_func=_update_bill_type,
        context=context,
    )
    context.info("BillTypes updated successfully")


def _update_bill_type(response_data: dict, context: TaskContext) -> None:
    """Signature: openapi_client.ItemFunc"""
    data = schema.BillType.model_validate(response_data)

    category, _ = BillTypeCategory.objects.get_or_create(name=data.category.name)

    BillType.objects.update_or_create(
        parliamentdotuk=data.id,
        defaults={
            "name": data.name,
            "description": data.description,
            "category": category,
        },
    )
