from celery import shared_task
from celery.utils import log as logging
from crawlers import caches
from crawlers.network import JsonCache, json_cache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from crawlers.parliamentdotuk.tasks.openapi.bills.billpublications import \
    fetch_and_update_bill_publications
from crawlers.parliamentdotuk.tasks.openapi.bills.billstages import \
    fetch_and_update_bill_stages
from crawlers.parliamentdotuk.tasks.openapi.bills.billstagetypes import \
    update_bill_stage_types
from crawlers.parliamentdotuk.tasks.openapi.bills.billtypes import \
    update_bill_types
from crawlers.parliamentdotuk.tasks.openapi.bills.update import update_bill
from notifications.models import TaskNotification
from notifications.models.task_notification import task_notification
from repository.models import Bill

log = logging.get_logger(__name__)


def _update_type_definitions(
    cache: JsonCache | None,
    notification: TaskNotification | None,
):
    """Must be run before fetch_and_update_bill."""
    update_bill_types(cache=cache, notification=notification)
    update_bill_stage_types(cache=cache, notification=notification)


@task_notification(label="Update individual bill")
@json_cache(caches.BILLS)
def fetch_and_update_bill(
    parliamentdotuk: int,
    cache: JsonCache | None,
    notification: TaskNotification | None,
) -> None:
    log.info(f"Updating bill #{parliamentdotuk}")
    openapi_client.get(
        endpoints.bill(parliamentdotuk),
        item_func=update_bill,
        notification=notification,
        cache=cache,
    )

    # Update related data for this bill
    fetch_and_update_bill_stages(parliamentdotuk, cache, notification)
    fetch_and_update_bill_publications(parliamentdotuk, cache, notification)
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


@shared_task
@task_notification(label="Update bills")
@json_cache(caches.BILLS)
def update_bills(
    cache: JsonCache | None,
    notification: TaskNotification | None,
    force_update: bool = False,
) -> None:
    _update_type_definitions(cache, notification)

    def _update_item_proxy(data: dict, _notification: TaskNotification | None) -> None:
        """
        Signature: openapi_client.ItemFunc

        endpoints.BILLS_ALL returns a list of schema.BillSummary objects. We need the full Bill,
        so need to retrieve the billId and make another request.
        """
        summary = schema.BillSummary(**data)

        if force_update or _should_update(summary):
            fetch_and_update_bill(
                summary.billId, cache=cache, notification=_notification
            )

    log.info("Updating all bills...")
    openapi_client.foreach(
        endpoints.BILLS_ALL,
        item_func=_update_item_proxy,
        cache=cache,
        notification=notification,
    )
    log.info("All bills updated successfully")
