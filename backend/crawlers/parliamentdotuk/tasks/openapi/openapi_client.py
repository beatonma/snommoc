from typing import Callable, Union

from crawlers.context import TaskContext
from crawlers.network import get_json
from crawlers.network.exceptions import HttpError
from pydantic import ValidationError

"""
ItemFunc receives:
- a dict of data returned by an API call,
- an TaskNotification which can be used to report progress or errors (may be None)
- a dict of additional kwargs which provide context data (may be None, or missing)
"""
type ItemFunc = Union[
    Callable[[dict, TaskContext, dict | None], None],
    Callable[[dict, TaskContext], None],
]


def _apply_item_func(
    item: dict,
    item_func: ItemFunc,
    context: TaskContext,
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
            item_func(item, context)
        else:
            item_func(item, context, func_kwargs)
        return True

    except HttpError as e:
        context.warning(f"Item response failed with status={e.status_code}: {report()}")
        return True

    except ValidationError as e:
        context.error(e, "Schema validation failed")
        raise e

    except Exception as e:
        context.warning(f"Failed to read item: {report()}")
        context.mark_as_failed(e)
        return False


def foreach(
    endpoint_url: str,
    item_func: ItemFunc,
    context: TaskContext,
    items_key: str = "items",
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
    item_count = context.skip_items
    items_per_page = context.items_per_page

    def _item_notification_info(_index: int):
        params = f"skip={item_count}&take={items_per_page}"

        return f"Item #{_index} of {endpoint_url}?{params}"

    while True:
        if context.is_finished():
            return
        data = get_json(
            endpoint_url,
            params={
                "skip": item_count,
                "take": items_per_page,
            },
            cache=context.cache,
            session=context.session,
        )
        # Data may be an object including pagination data, or just a list of items
        data_is_dict = isinstance(data, dict)

        if data_is_dict:
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
            should_continue = _apply_item_func(
                item,
                item_func,
                context,
                lambda: _item_notification_info(index),
                func_kwargs,
            )
            if not should_continue:
                return

            item_count += 1
            if context.limit_reached(item_count):
                return

        if data_is_dict:
            if item_count >= data.get("totalResults", 0):
                break


def get(
    endpoint_url: str,
    item_func: ItemFunc,
    context: TaskContext,
    func_kwargs: dict | None = None,
):
    """
    Retrieve a dictionary JSON object from endpoint_url and pass it to item_func for processing.
    """
    item = get_json(
        endpoint_url,
        cache=context.cache,
        session=context.session,
    )

    if not isinstance(item, dict):
        raise TypeError(
            f"openapi_client.get expects a response with a dictionary, got {item}"
        )

    _apply_item_func(
        item,
        item_func,
        context,
        lambda: endpoint_url,
        func_kwargs,
    )
