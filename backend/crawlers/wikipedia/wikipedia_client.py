from typing import Callable, Type
from urllib.parse import urlencode

from crawlers.context import TaskContext
from crawlers.network import get_json
from crawlers.wikipedia import endpoints
from crawlers.wikipedia.tasks import schema

"""
When making many queries, create batches to reduce number of requests:
https://www.mediawiki.org/wiki/API:Etiquette
"""
BATCH_SIZE = 5

default_params = {
    "action": "query",
    "format": "json",
    "pilicense": "free",
    "maxlag": 2,
}


def for_each_page[T](
    page_titles: list[str],
    block: Callable[[str, T], None],
    page_class: Type[T],
    context: TaskContext,
    batch_size: int = BATCH_SIZE,
    **params,
):
    """
    Run the given [block] on the API response retrieved for the given page titles.
    """
    item_count = 0
    for batch in _chunks(page_titles, batch_size):
        normalized, pages = _get_batch_pages(batch, page_class, context, **params)

        for page in pages:
            t = page.title
            title = normalized[t] if t in normalized else t

            block(title, page)

            item_count += 1
            if context.limit_reached(item_count):
                return

        if not context.follow_pagination:
            context.info("Task is not following pagination.")
            return


def _chunks(lst: list[str], size: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def _get_batch_pages[T: schema.Page](
    batch, t: Type[T], context: TaskContext, **params
) -> tuple[dict, list[T]]:
    """
    Get data for a batch of page titles.
    Returns a dictionary with corrected page titles, and the list of page data.
    """
    batch_pages = "|".join(batch)

    encoded_params = urlencode(
        {"titles": batch_pages, **default_params, **params},
        safe=r"|",
    )

    response = get_json(
        endpoints.WIKIPEDIA_API,
        dangerous_encoded_params=encoded_params,
        cache=context.cache,
        session=context.session,
    )
    data = schema.BatchResponse[t].model_validate(response).query

    normalized = _map_normalized(data.normalized)
    pages = list(data.pages.values())

    return normalized, pages


def _map_normalized(normalized: list[schema.Normalized] | None) -> dict[str, str]:
    if normalized:
        return {item.to: item.original for item in normalized}
    else:
        return {}
