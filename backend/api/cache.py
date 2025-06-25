import logging
from datetime import timedelta
from functools import wraps

from crawlers.caches import API_VIEW_CACHE
from django.views.decorators.cache import cache_page
from ninja.decorators import decorate_view

log = logging.getLogger(__name__)


def cache_view(_func=None, *, timeout: float, cache_key: str):
    def decorator_factory(func):
        @wraps(func)
        @decorate_view(cache_page(timeout=timeout, key_prefix=cache_key))
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped_func

    if _func:
        return decorator_factory(_func)
    return decorator_factory


def cache_crawled_data_view(
    _func=None,
    *,
    timeout: float = timedelta(days=7).total_seconds(),
    cache_key=API_VIEW_CACHE,
):
    return cache_view(_func, timeout=timeout, cache_key=cache_key)
