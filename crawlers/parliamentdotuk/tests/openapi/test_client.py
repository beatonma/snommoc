from typing import Optional

import crawlers
from basetest.testcase import NetworkTestCase
from crawlers.network.cache import create_json_cache
from crawlers.parliamentdotuk.tasks.openapi import openapi_client
from notifications.models import TaskNotification


class ClientTestCase(NetworkTestCase):
    def test_client_foreach_with_list_response(self):
        """Test foreach when the endpoint returns an unwrapped list of items."""
        items_processed = 0
        division_id = None

        def item_func(data: dict, notification: Optional[TaskNotification]) -> None:
            nonlocal items_processed, division_id
            items_processed = items_processed + 1
            division_id = data.get("divisionId")

        print(crawlers.network.get_json)

        openapi_client.foreach(
            "https://lordsvotes-api.parliament.uk/data/Divisions/search",
            cache=create_json_cache("openapi-tests"),
            notification=TaskNotification(title="ClientTestCase"),
            item_func=item_func,
            items_per_page=1,
            max_items=1,
        )

        self.assertEqual(items_processed, 1)

        # The actual value of division_id will change over time depending on response data, but should always be an integer.
        self.assertIsNotNone(division_id)
        self.assertTrue(isinstance(division_id, int))

    def test_client_foreach_with_wrapped_response(self):
        """Test foreach when the endpoint returns a dictionary with an 'items' child list."""
        items_processed = 0
        bill_id = None

        def item_func(data: dict, notification: Optional[TaskNotification]) -> None:
            nonlocal items_processed, bill_id
            items_processed = items_processed + 1
            bill_id = data.get("billId")

        print(crawlers.network.get_json)

        openapi_client.foreach(
            "https://bills-api.parliament.uk/api/v1/Bills",
            cache=create_json_cache("openapi-tests"),
            notification=TaskNotification(title="ClientTestCase"),
            item_func=item_func,
            items_per_page=1,
            max_items=1,
        )

        self.assertEqual(items_processed, 1)

        # The actual value of bill_id will change over time depending on response data, but should always be an integer.
        self.assertIsNotNone(bill_id)
        self.assertTrue(isinstance(bill_id, int))
