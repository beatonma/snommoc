import datetime
import os
import shutil

from django.conf import settings

from basetest.testcase import LocalTestCase

from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_cache import (
    JsonResponseCache,
    _url_to_filename,
)


class MdpCacheTest(LocalTestCase):
    cache_name = "mdp-cache-test"

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

        now = datetime.datetime.now()
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
