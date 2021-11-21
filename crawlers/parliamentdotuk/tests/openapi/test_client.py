import crawlers
from basetest.testcase import NetworkTestCase
from crawlers.network.cache import create_json_cache
from crawlers.parliamentdotuk.tasks.openapi import openapi_client
from notifications.models import TaskNotification


class ClientTestCase(NetworkTestCase):
    def test_client__foreach(self):
        items_processed = 0

        def item_func(data: dict) -> None:
            nonlocal items_processed
            items_processed = items_processed + 1

        print(crawlers.network.get_json)

        openapi_client.foreach(
            "https://lordsvotes-api.parliament.uk/data/Divisions/search",
            cache=create_json_cache("openapi"),
            notification=TaskNotification(title="ClientTestCase"),
            item_func=item_func,
            items_per_page=1,
            max_items=1,
        )

        self.assertEqual(items_processed, 1)
