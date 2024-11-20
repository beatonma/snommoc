from celery.utils import log as logging
from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from crawlers.parliamentdotuk.tasks.openapi.bills.billpublications import (
    fetch_and_update_bill_publications,
)
from crawlers.parliamentdotuk.tasks.openapi.bills.billstages import (
    fetch_and_update_bill_stages,
)
from crawlers.parliamentdotuk.tasks.openapi.bills.billstagetypes import (
    update_bill_stage_types,
)
from crawlers.parliamentdotuk.tasks.openapi.bills.billtypes import update_bill_types
from crawlers.parliamentdotuk.tasks.openapi.bills.update import update_bill
from repository.models import Bill

log = logging.get_logger(__name__)


def update_billtype_definitions(context: TaskContext):
    """Must be run before fetch_and_update_bill."""
    update_bill_types(context=context)
    update_bill_stage_types(context=context)


@task_context(cache_name=caches.BILLS, label="Update individual bill")
def fetch_and_update_bill(parliamentdotuk: int, context: TaskContext) -> None:
    log.info(f"Updating bill #{parliamentdotuk}")
    openapi_client.get(
        endpoints.bill(parliamentdotuk),
        item_func=update_bill,
        context=context,
    )

    # Update related data for this bill
    fetch_and_update_bill_stages(parliamentdotuk, context)
    fetch_and_update_bill_publications(parliamentdotuk, context)
    log.info(f"Bill #{parliamentdotuk} updated successfully")


def _should_update(summary: schema.BillSummary) -> bool:
    """Return True if last_update value differs from what we already have recorded"""
    _id = summary.billId
    try:
        bill = Bill.objects.get(parliamentdotuk=_id)
        if bill.last_update == summary.lastUpdate:
            # Our Bill is up-to-date, no need to go further.
            log.info(
                f"Skipping bill #{_id} is already up-to-date"
                f" (last_update={bill.last_update})."
            )
            return False

    except:
        # Bill does not exist in our database so continue to fetch it.
        pass

    return True


@task_context(cache_name=caches.BILLS, label="Update bills")
def update_bills(context: TaskContext) -> None:
    update_billtype_definitions(context)

    def _update_item_proxy(
        data: dict,
        _context: TaskContext,
    ) -> None:
        """
        Signature: openapi_client.ItemFunc

        endpoints.BILLS_ALL returns a list of schema.BillSummary objects. We need the full Bill,
        so need to retrieve the billId and make another request.
        """
        summary = schema.BillSummary(**data)

        if _context.force_update or _should_update(summary):
            fetch_and_update_bill(summary.billId, context=_context)

    log.info("Updating all bills...")
    openapi_client.foreach(
        endpoints.BILLS_ALL,
        item_func=_update_item_proxy,
        context=context,
    )
    log.info("All bills updated successfully")
