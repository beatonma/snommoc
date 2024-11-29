from typing import Callable, Literal, Union

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
type ItemFunc[T] = Union[
    Callable[[dict, TaskContext, dict | None], T],
    Callable[[dict, TaskContext], T],
]


type ItemFuncStatus = Literal["continue", "exit"]


def _apply_item_func[
    T
](
    item: dict,
    item_func: ItemFunc[T],
    context: TaskContext,
    report: Callable[[], str],
    func_kwargs: dict | None,
) -> (T | ItemFuncStatus):
    """
    :param report: A function that describes the item for useful error logging.
    :return: True if the caller should continue its task, False if the caller should halt the task.
             HttpError will log a warning but allow the caller to continue.
    """

    try:
        if func_kwargs is None:
            return item_func(item, context)
        else:
            return item_func(item, context, func_kwargs)

    except HttpError as e:
        context.warning(
            f"Item response failed with status={e.status_code}: {report()}\n{e}"
        )
        return "exit"

    except ValidationError as e:
        context.error(e, "Schema validation failed")
        raise e

    except Exception as e:
        context.error(e, f"Failed to read item: {report()}")
        context.mark_as_failed(e)
        raise e


def foreach(
    endpoint_url: str,
    item_func: ItemFunc,
    context: TaskContext,
    items_key: str = "items",
    func_kwargs: dict | None = None,
) -> None:
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

    while True:
        if context.is_finished():
            context.warning(
                f"Context marked as done: complete={context.complete} | failed={context.failed}"
            )
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
                "openapi_client.foreach expects a response with a list of items, "
                f"got {data}"
            )

        if len(items) == 0:
            return

        for index, item in enumerate(items):
            func_status = _apply_item_func(
                item,
                item_func,
                context,
                lambda: f"Item #{index} of {endpoint_url}?skip={item_count}&take={items_per_page}",
                func_kwargs,
            )
            if func_status == "exit":
                return

            item_count += 1
            if context.limit_reached(item_count):
                return

        if not context.follow_pagination:
            context.info("Task is not following pagination.")
            return

        if data_is_dict and item_count >= data.get("totalResults", 0):
            context.info(f"Finished updating {item_count} items")
            return


def get[
    T
](
    endpoint_url: str,
    item_func: ItemFunc[T],
    context: TaskContext,
    func_kwargs: dict | None = None,
) -> T:
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

    return _apply_item_func(
        item,
        item_func,
        context,
        lambda: endpoint_url,
        func_kwargs,
    )
