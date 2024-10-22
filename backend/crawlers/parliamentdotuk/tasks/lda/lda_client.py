from typing import Callable, Type

from celery.utils.log import get_task_logger
from crawlers.context import TaskContext
from crawlers.network import get_json
from crawlers.network.exceptions import HttpError
from crawlers.parliamentdotuk.tasks.lda.endpoints import debug_url
from crawlers.parliamentdotuk.tasks.lda.schema import Item, Page
from crawlers.parliamentdotuk.tasks.util.checks import MissingFieldException
from pydantic import BaseModel as Schema

PARAM_PAGE_SIZE = "_pageSize"
PARAM_PAGE = "_page"
MAX_PAGE_SIZE = 100

log = get_task_logger(__name__)


type ItemFunc[T: Schema] = Callable[[T, TaskContext], None]


def get_item_data[T: Schema](type: Type[T], endpoint: str, context: TaskContext) -> T:
    data = get_json(endpoint, cache=context.cache, session=context.session)

    return Item[type].model_validate(data).data


def foreach[
    T: Schema
](
    endpoint_url: str,
    item_schema_type: Type[T],
    item_func: ItemFunc[T],
    context: TaskContext,
    page_size=MAX_PAGE_SIZE,
    follow_pagination: bool = True,
) -> None:
    """
    Retrieve a JSON list from endpoint_url and pass each item to item_func for processing.
    Paging is handled automatically until no more items are returned, or max_items count is reached (if specified).
    """
    page_number = 0
    next_page = "no-next-page-placeholder"

    notification = context.notification

    def _item_notification_info(_index: int) -> str:
        url = debug_url(
            endpoint_url, **{PARAM_PAGE: page_number, PARAM_PAGE_SIZE: page_size}
        )
        return f"Item #{_index}: {context.notification.html_link(url)})"

    while next_page is not None:
        data = get_json(
            endpoint_url,
            params={
                PARAM_PAGE_SIZE: page_size,
                PARAM_PAGE: page_number,
            },
            cache=context.cache,
        )
        page = Page[item_schema_type].model_validate(data)

        for index, item in enumerate(page.items):
            try:
                item_func(item, context)

            except MissingFieldException as e:
                notification.warning(
                    f"Item response is missing required data and will be skipped [{_item_notification_info(index)}]: {e}"
                )
                continue

            except HttpError as e:
                notification.warning(
                    f"Item response failed with status={e.status_code} [{_item_notification_info(index)}]"
                )
                continue

            except Exception as e:
                notification.warning(
                    f"Failed to read item: [{_item_notification_info(index)}]"
                )
                notification.mark_as_failed(e)
                return

        page_number += 1
        next_page = page.next_page_url if follow_pagination else None
