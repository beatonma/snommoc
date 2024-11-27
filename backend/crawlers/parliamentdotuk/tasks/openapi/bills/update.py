from celery.utils import log as logging
from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from crawlers.parliamentdotuk.tasks.openapi.bills.bill import update_bill
from crawlers.parliamentdotuk.tasks.openapi.bills.billstages import (
    fetch_and_update_bill_stages,
    update_bill_stage_types,
)
from crawlers.parliamentdotuk.tasks.openapi.bills.billtypes import update_bill_types
from crawlers.parliamentdotuk.tasks.openapi.bills.publications import (
    fetch_and_update_bill_publications,
)
from repository.models import Bill


@task_context(cache_name=caches.BILLS, label="Update bills")
def update_bills(context: TaskContext) -> None:
    _update_billtype_definitions(context)

    def _update_item_proxy(data: dict, _context: TaskContext):
        """
        Signature: openapi_client.ItemFunc

        endpoints.BILLS_ALL returns a list of schema.BillSummary objects. We need the full Bill,
        so need to retrieve the billId and make another request.
        """
        summary = schema.BillSummary.model_validate(data)

        if _context.force_update or _should_update(summary):
            _fetch_and_update_bill(summary.bill_id, context=_context)

    openapi_client.foreach(
        endpoints.BILLS_ALL,
        item_func=_update_item_proxy,
        context=context,
    )


def _update_billtype_definitions(context: TaskContext):
    """Must be run before fetch_and_update_bill."""
    update_bill_types(context=context)
    update_bill_stage_types(context=context)


def _fetch_and_update_bill(parliamentdotuk: int, context: TaskContext) -> None:
    openapi_client.get(
        endpoints.bill(parliamentdotuk),
        item_func=update_bill,
        context=context,
    )

    # Update related data for this bill
    fetch_and_update_bill_stages(parliamentdotuk, context)
    fetch_and_update_bill_publications(parliamentdotuk, context)
    context.info(f"Bill #{parliamentdotuk} updated successfully")


def _should_update(summary: schema.BillSummary) -> bool:
    """Return True if last_update value differs from what we already have recorded"""
    _id = summary.bill_id
    try:
        bill = Bill.objects.get(parliamentdotuk=_id)
        if bill.last_update == summary.last_update:
            # Our Bill is up-to-date, no need to go further.
            return False

    except:
        # Bill does not exist in our database so continue to fetch it.
        pass

    return True
