from datetime import timedelta
from typing import Callable, List, TypeVar, Iterable
from urllib.parse import urlencode

from crawlers.network import get_json

from crawlers.wikipedia import endpoints
from crawlers.network import json_cache


CACHE_TTL = int(timedelta(days=7).total_seconds())

"""
When making many queries, create batches to reduce number of requests:
https://www.mediawiki.org/wiki/API:Etiquette
"""
BATCH_SIZE = 5

default_params = {
    "action": "query",
    "format": "json",
    "pilicense": "free",
}

T = TypeVar("T")


def for_pages(
    page_titles: List[str],
    block: Callable[[str, dict], None],
    batch_size: int = BATCH_SIZE,
    **params,
):
    for batch in _chunks(page_titles, batch_size):
        normalized, pages = _get_batch_pages(batch, **params)

        for page in pages:
            t = page["title"]
            title = normalized[t] if t in normalized else t

            block(title, page)


def get_for_pages(
    page_titles: List[str],
    block: Callable[[str, dict], T],
    batch_size: int = BATCH_SIZE,
    **params,
) -> Iterable[T]:
    for batch in _chunks(page_titles, batch_size):
        normalized, pages = _get_batch_pages(batch, **params)

        for page in pages:
            t = page["title"]
            title = normalized[t] if t in normalized else t

            yield block(title, page)


def _chunks(lst: list, size: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


@json_cache(name="wikipedia", ttl_seconds=CACHE_TTL)
def _get_wikipedia_api(
    params,
    dangerous_encoded_params: bool = False,
    **kwargs,
) -> dict:
    return get_json(
        endpoints.WIKIPEDIA_API,
        params=params,
        dangerous_encoded_params=dangerous_encoded_params,
        **kwargs,
    )


def _get_batch_pages(batch, **params):
    batch_pages = "|".join(batch)

    encoded_params = urlencode(
        {"titles": batch_pages, **default_params, **params},
        safe=r"|",
    )

    data = _get_wikipedia_api(
        encoded_params,
        dangerous_encoded_params=True,
    )["query"]
    normalized = _map_normalized(data["normalized"])
    pages = list(data["pages"].values())

    return (normalized, pages)


def _map_normalized(normalized: list) -> dict:
    return {item["to"]: item["from"] for item in normalized}