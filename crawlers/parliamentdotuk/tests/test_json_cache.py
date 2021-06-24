import datetime
import os
import shutil

from django.conf import settings

from basetest.testcase import LocalTestCase

from crawlers.network.cache import (
    JsonResponseCache,
    _url_to_filename,
    json_cache,
)
from util.time import get_now


class JsonCacheTest(LocalTestCase):
    """JsonResponseCache tests"""

    cache_name = "json-cache-test"

    def test__url_to_filename(self):
        url = "http://data.parliament.uk/membersdataplatform/services/mnis/members/query/id=2451/FullBiog/"
        filename = _url_to_filename(url)

        self.assertEqual(
            filename,
            "membersdataplatform-services-mnis-members-query-id=2451-FullBiog-.json",
        )

    def test_cache_is_correct(self):
        cache = JsonResponseCache(self.cache_name, time_to_live_seconds=1000)

        url = "https://parliament.uk/example/request/data.json"
        data = {"a": 3, "b": 19}

        self.assertIsNone(cache.get_json(url))

        cache.remember(url, data)

        cached_data = cache.get_json(url)
        self.assertDictEqual(data, cached_data)

    def test_cache_time_to_live_is_correct(self):
        url = "https://parliament.uk/example/request/data.json"
        data = {"a": 5, "b": 17}

        now = get_now()
        live_cache_timestamp = now + datetime.timedelta(minutes=55)
        expired_timestamp = now + datetime.timedelta(minutes=65)

        ttl = datetime.timedelta(minutes=60).total_seconds()

        cache = JsonResponseCache(self.cache_name, time_to_live_seconds=ttl, now=now)
        cache.remember(url, data)
        cache.finish(now=now)

        live_cache = JsonResponseCache(
            self.cache_name, time_to_live_seconds=ttl, now=live_cache_timestamp
        )
        self.assertDictEqual(live_cache.get_json(url), data)

        # Cache should be flushed as previous timestamp is more than [ttl] seconds in the past.
        expired_cache = JsonResponseCache(
            self.cache_name, time_to_live_seconds=ttl, now=expired_timestamp
        )
        self.assertIsNone(expired_cache.get_json(url))

    def tearDown(self) -> None:
        cache_dir = os.path.join(settings.CRAWLER_CACHE_ROOT, self.cache_name)
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)


class JsonCacheDecoratorTest(LocalTestCase):
    """@json_cache decorator tests"""

    root_url = "https://snommoc.org/example/request/root.json"
    root_data = {"abc": 123}

    child_url = "https://snommoc.org/example/request/child.json"
    child_data = {"def": 456}

    @json_cache(name="decorated-root")
    def decorated_root(self, **kwargs):
        kwargs["cache"].remember(self.root_url, self.root_data)
        self.decorated_child(**kwargs)

    @json_cache(name="decorated-child")
    def decorated_child(self, **kwargs):
        kwargs["cache"].remember(self.child_url, self.child_data)

    def _get_cache_path(self, name, url):
        dir = os.path.join(settings.CRAWLER_CACHE_ROOT, name)
        if not url:
            return dir

        filename = _url_to_filename(url)
        return os.path.join(dir, filename)

    def test_json_cache_decorator__data_is_retrievable(self):
        self.decorated_child()

        cache = JsonResponseCache("decorated-child")
        self.assertDictEqual(cache.get_json(self.child_url), self.child_data)

    def test_json_cache_decorator_nested__should_share_root_cache(self):
        self.decorated_root()

        cache = JsonResponseCache("decorated-root")
        self.assertDictEqual(cache.get_json(self.root_url), self.root_data)
        self.assertDictEqual(cache.get_json(self.child_url), self.child_data)

        self.assertFalse(os.path.exists(self._get_cache_path("decorated-child", "")))

    def tearDown(self) -> None:
        dirs = ["decorated-root", "decorated-child"]

        for d in dirs:
            cache_dir = os.path.join(settings.CRAWLER_CACHE_ROOT, d)
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
