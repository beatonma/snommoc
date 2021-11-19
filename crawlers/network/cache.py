import datetime
import hashlib
import json
import logging
import os
from functools import wraps
from typing import Optional

from django.conf import settings
from django.utils import timezone

from util import settings_contract
from util.settings import get_cache_settings
from util.time import get_now, coerce_timezone

log = logging.getLogger(__name__)

TIME_TO_LIVE_DEFAULT = get_cache_settings().get(
    settings_contract.CACHE_CRAWLER_TTL,
    datetime.timedelta(days=4).total_seconds(),
)


def _url_to_filename(url: str) -> str:
    """Convert a url to a safe filename.

    By hashing with sha1 we get a reproducible 45 character (hash + extension) filename with safe characters.
    """
    hashed = hashlib.sha1(url.encode()).hexdigest()

    return f"{hashed}.json"


class JsonResponseCache:
    """
    Simple file cache for storing JSON data from network responses.
    """

    def __init__(
        self,
        name,
        time_to_live_seconds=TIME_TO_LIVE_DEFAULT,
        now=get_now,
    ):
        if callable(now):
            now = now()

        root = settings.CRAWLER_CACHE_ROOT
        self.cache_dir = os.path.join(root, name)
        self.time_to_live = time_to_live_seconds or TIME_TO_LIVE_DEFAULT

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        if self._cache_is_expired(now=now):
            self._flush()

    def get_json(self, url) -> Optional[dict]:
        """Return cached JSON for the given url if it exists."""
        filepath = self._get_filepath(url)

        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, TypeError) as e:
                log.warning(f"Unable to read JSON from cache file {filepath}")

    def remember(self, url: str, json_data: dict) -> None:
        """Store JSON in the cache"""
        filepath = self._get_filepath(url)

        with open(filepath, "w") as f:
            json.dump(json_data, f)

    def finish(self, now=get_now):
        """Remember the timestamp so we can use time_to_live to determine whether
        we should use the cache next time."""
        if callable(now):
            now = now()
        data = {"timestamp": now.isoformat()}
        with open(self._get_meta_filepath(), "w") as f:
            json.dump(data, f)

    def _get_meta_filepath(self):
        return os.path.join(self.cache_dir, "cache.json")

    def _get_filepath(self, url) -> str:
        return os.path.join(self.cache_dir, _url_to_filename(url))

    def _cache_is_expired(self, now: datetime.datetime) -> bool:
        """Return True if the previous cache timestamp is more than time_to_live seconds in the past"""

        try:
            with open(self._get_meta_filepath(), "r") as f:
                previous_timestamp_str = json.load(f).get("timestamp")
        except:
            # Could not read the previous timestamp - assume cache is old.
            return True

        previous_timestamp = coerce_timezone(
            timezone.datetime.fromisoformat(previous_timestamp_str)
        )

        delta = now - previous_timestamp

        if delta.total_seconds() >= self.time_to_live:
            log.info(
                f"Cache has expired (age={delta.total_seconds()} seconds, ttl={self.time_to_live})"
            )
            return True

        return False

    def _flush(self):
        for f in [x for x in os.listdir(self.cache_dir) if x.endswith(".json")]:
            filepath = os.path.join(self.cache_dir, f)
            os.remove(filepath)


def json_cache(
    name: str,
    ttl_seconds: int = TIME_TO_LIVE_DEFAULT,
    now=get_now,
):
    """
    Apply the @json_cache decoration to a function to define the name of the cache used by
    any network calls spawned from it.
    """

    def cached_call(func):
        @wraps(func)
        def using_cache(*args, **kwargs):
            # Check if a cache is already in use by caller
            is_root = "cache" not in kwargs
            result = None

            if is_root:
                cache = create_json_cache(
                    name=name,
                    ttl_seconds=ttl_seconds,
                    now=now,
                )
                kwargs["cache"] = cache

            try:
                result = func(*args, **kwargs)

            except Exception as e:
                log.warning(e)

            finally:
                if is_root:
                    cache = kwargs["cache"]
                    if cache:
                        cache.finish()

            return result

        return using_cache

    return cached_call


def create_json_cache(
    name: str,
    ttl_seconds: int = TIME_TO_LIVE_DEFAULT,
    now=get_now,
) -> JsonResponseCache:
    return JsonResponseCache(
        name,
        ttl_seconds,
        now() if callable(now) else now,
    )
