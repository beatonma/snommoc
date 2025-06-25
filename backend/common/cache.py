import logging

from django.conf import settings
from django.core.cache import cache

log = logging.getLogger(__name__)


def invalidate_cache(cache_key: str):
    try:
        cache.delete_pattern(f"*{cache_key}*")
    except AttributeError:
        if not settings.DEBUG:
            log.warning(f"Failed to invalidate cache '{cache_key}'")
