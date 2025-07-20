import logging

from django.conf import settings
from django.core.cache import cache

log = logging.getLogger(__name__)


def invalidate_cache(cache_key: str):
    try:
        if count := cache.delete_pattern(f"*{cache_key}*"):
            log.info(f"Deleted {count} items from the cache.")
    except AttributeError:
        if not settings.DEBUG:
            log.warning(f"Failed to invalidate cache '{cache_key}'")
