from typing import Callable, Union

import requests
from crawlers.network import JsonResponseCache, get_json
from crawlers.network.exceptions import HttpError
from notifications.models import TaskNotification

"""
ItemFunc receives:
- a dict of data returned by an API call,
- an TaskNotification which can be used to report progress or errors (may be None)
- a dict of additional kwargs which provide context data (may be None, or missing)
"""
type ItemFunc = Union[
    Callable[[dict, TaskNotification | None, dict | None], None],
    Callable[[dict, TaskNotification | None], None],
]


def _apply_item_func(
    item: dict,
    item_func: ItemFunc,
    notification: TaskNotification | None,
    report: Callable[[], str],
    func_kwargs: dict | None,
) -> bool:
    """
    :param report: A function that describes the item for useful error logging.
    :return: True if the caller should continue its task, False if the caller should halt the task.
             HttpError will log a warning but allow the caller to continue.
    """

    try:
        if func_kwargs is None:
            item_func(item, notification)
        else:
            item_func(item, notification, func_kwargs)
        return True

    except HttpError as e:
        if notification:
            notification.warning(
                f"Item response failed with status={e.status_code}: {report()}"
            )
        return True

    except Exception as e:
        if notification:
            notification.warning(f"Failed to read item: {report()}")
            notification.mark_as_failed(e)
        return False


def foreach(
    endpoint_url: str,
    item_func: ItemFunc,
    notification: TaskNotification | None,
    cache: JsonResponseCache | None,
    items_key: str = "items",
    items_per_page: int = 25,
    max_items: int | None = None,
    func_kwargs: dict | None = None,
):
    """
    Retrieve a JSON list from endpoint_url and pass each item to item_func for processing.
    Paging is handled automatically until no more items are returned, or max_items count is reached (if specified).

    Endpoints may return a JSON list of items, or a JSON object with an 'items' child list.

    Handled responses:
        - [...]
        - {
            "items": [...],
            ...
          }
    """
    item_count = 0

    def _item_notification_info(index: int):
        params = f"skip={item_count}&take={items_per_page}"

        return f"Item #{index} of {endpoint_url}?{params}"

    with requests.Session() as session:
        while True:
            data = get_json(
                endpoint_url,
                params={
                    "skip": item_count,
                    "take": items_per_page,
                },
                cache=cache,
                session=session,
            )

            if isinstance(data, dict):
                # Unwrap the items list.
                items = data.get(items_key)
            else:
                items = data

            if not isinstance(items, list):
                raise TypeError(
                    "openapi_client.foreach expects a response with a list of items, got"
                    f" {data}"
                )

            if len(items) == 0:
                break

            for index, item in enumerate(items):
                _apply_item_func(
                    item,
                    item_func,
                    notification,
                    lambda: _item_notification_info(index),
                    func_kwargs,
                )

                item_count += 1
                if max_items is not None:
                    if item_count >= max_items:
                        if notification:
                            notification.append(f"max_items={max_items} limit reached.")
                        return

            if "totalResults" not in data or "itemsPerPage" not in data:
                # Exit if data is not paginated.
                break

            if item_count >= data["totalResults"] or len(items) < items_per_page:
                break


def get(
    endpoint_url: str,
    item_func: ItemFunc,
    notification: TaskNotification | None,
    cache: JsonResponseCache | None,
    func_kwargs: dict | None = None,
):
    """
    Retrieve a dictionary JSON object from endpoint_url and pass it to item_func for processing.
    """
    item = get_json(
        endpoint_url,
        cache=cache,
    )

    if not isinstance(item, dict):
        raise TypeError(
            f"openapi_client.get expects a response with a dictionary, got {item}"
        )

    _apply_item_func(
        item,
        item_func,
        notification,
        lambda: endpoint_url,
        func_kwargs,
    )
