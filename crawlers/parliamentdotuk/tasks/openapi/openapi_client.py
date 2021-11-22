from typing import Callable, Dict, Optional

from crawlers.network import JsonResponseCache, get_json
from crawlers.network.exceptions import HttpError
from notifications.models import TaskNotification


def foreach(
    endpoint_url: str,
    item_func: Callable[[Dict, Optional[TaskNotification]], None],
    notification: Optional[TaskNotification],
    cache: Optional[JsonResponseCache],
    items_per_page: int = 25,
    max_items: Optional[int] = None,
):
    item_count = 0

    def _item_notification_info(index: int):
        params = f"skip={item_count}&take={items_per_page}"

        return f"Item #{index} of {endpoint_url}?{params}"

    while True:
        items = get_json(
            endpoint_url,
            params={
                "skip": item_count,
                "take": items_per_page,
            },
            cache=cache,
        )

        if not isinstance(items, list):
            raise TypeError(
                f"openapi_client.foreach expects a response with a list of items, got {items}"
            )

        if len(items) == 0:
            break

        for index, item in enumerate(items):
            try:
                item_func(item)

            except HttpError as e:
                if notification:
                    notification.warning(
                        f"Item response failed with status={e.status_code}: {_item_notification_info(index)}"
                    )

            except Exception as e:
                if notification:
                    notification.warning(
                        f"Failed to read item: {_item_notification_info(index)}"
                    )
                    notification.mark_as_failed(e)
                return

            item_count = item_count + 1
            if max_items is not None:
                if item_count >= max_items:
                    if notification:
                        notification.append(f"max_items={max_items} limit reached.")
                    return
