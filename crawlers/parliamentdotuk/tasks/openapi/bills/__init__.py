from typing import Optional

from crawlers import caches
from crawlers.network import JsonResponseCache, json_cache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import viewmodels
from crawlers.parliamentdotuk.tasks.openapi.bills.billstages import (
    fetch_and_update_bill_stages,
)
from crawlers.parliamentdotuk.tasks.openapi.bills.billstagetypes import (
    update_bill_stage_types,
)
from crawlers.parliamentdotuk.tasks.openapi.bills.billtypes import update_bill_types
from crawlers.parliamentdotuk.tasks.openapi.bills.update import (
    _update_bill,
)
from notifications.models import TaskNotification


@json_cache(caches.BILLS)
def fetch_and_update_bill(
    parliamentdotuk: int,
    cache: Optional[JsonResponseCache],
    notification: Optional[TaskNotification],
) -> None:
    openapi_client.get(
        endpoints.bill(parliamentdotuk),
        item_func=_update_bill,
        notification=notification,
        cache=cache,
    )

    fetch_and_update_bill_stages(parliamentdotuk, cache, notification)


@json_cache(caches.BILLS)
def update_bills(
    cache: Optional[JsonResponseCache],
    notification: Optional[TaskNotification],
    force: bool = False,  # TODO check bill last_update
) -> None:
    # TODO update sessions?
    update_bill_types(cache=cache, notification=notification)
    update_bill_stage_types(cache=cache, notification=notification)

    def _update_item_proxy(dict, notification) -> None:
        """
        endpoints.BILLS_ALL returns a list of viewmodels.BillSummary objects. We need the full Bill,
        so need to retrieve the billId and make another request.
        """
        summary = viewmodels.BillSummary(**dict)
        fetch_and_update_bill(summary.billId, cache=cache, notification=notification)

    openapi_client.foreach(
        endpoints.BILLS_ALL,
        item_func=_update_item_proxy,
        cache=cache,
        notification=notification,
    )
