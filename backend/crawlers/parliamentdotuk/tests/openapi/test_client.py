from unittest.mock import Mock, patch

from basetest.testcase import LocalTestCase, NetworkTestCase
from crawlers.network.cache import create_json_cache
from crawlers.parliamentdotuk.tasks.openapi import openapi_client
from crawlers.parliamentdotuk.tests.openapi.data_response import (
    UNWRAPPED_DIVISIONS_RESPONSE,
    WRAPPED_BILLS_RESPONSE,
    WRAPPED_PUBLICATIONS_RESPONSE,
)
from notifications.models import TaskNotification

MOCK_RESPONSES = {
    "https://bills-api.parliament.uk/api/v1/Bills/512/Publications": WRAPPED_PUBLICATIONS_RESPONSE,
    "https://lordsvotes-api.parliament.uk/data/Divisions/search": UNWRAPPED_DIVISIONS_RESPONSE,
    "https://bills-api.parliament.uk/api/v1/Bills": WRAPPED_BILLS_RESPONSE,
}


def _patch_get_json(**kwargs):
    return patch.object(
        openapi_client,
        "get_json",
        Mock(side_effect=lambda url, **kw: MOCK_RESPONSES.get(url)),
    )


class ClientTestCase(LocalTestCase):
    def test_client_foreach_with_list_response(self):
        """Test foreach when the endpoint returns an unwrapped list of items."""
        items_processed = 0
        division_id = None

        def item_func(data: dict, _: TaskNotification | None) -> None:
            """Signature: openapi_client.ItemFunc"""
            nonlocal items_processed, division_id
            items_processed += 1
            division_id = data.get("divisionId")

        with _patch_get_json():
            openapi_client.foreach(
                "https://lordsvotes-api.parliament.uk/data/Divisions/search",
                cache=create_json_cache("openapi-tests"),
                notification=TaskNotification(title="ClientTestCase"),
                item_func=item_func,
                items_per_page=1,
                max_items=1,
            )

        self.assertEqual(items_processed, 1)
        self.assertEqual(division_id, 2684)

    def test_client_foreach_with_wrapped_response(self):
        """Test foreach when the endpoint returns a dictionary with an 'items' child list."""
        items_processed = 0
        bill_id = None

        def item_func(data: dict, _: TaskNotification | None) -> None:
            nonlocal items_processed, bill_id
            items_processed += 1
            bill_id = data.get("billId")

        with _patch_get_json():
            openapi_client.foreach(
                "https://bills-api.parliament.uk/api/v1/Bills",
                cache=create_json_cache("openapi-tests"),
                notification=TaskNotification(title="ClientTestCase"),
                item_func=item_func,
                items_per_page=1,
                max_items=1,
            )

        self.assertEqual(items_processed, 1)
        self.assertEqual(bill_id, 2818)

    def test_client_with_wrapped_response(self):
        """Test foreach when the endpoint returns a dictionary with a child list with non-standard key."""
        publication_id = None

        def item_func(data: dict, _) -> None:
            """Signature: openapi_client.ItemFunc"""
            nonlocal publication_id
            publication_id = data.get("id")

        with _patch_get_json():
            openapi_client.foreach(
                "https://bills-api.parliament.uk/api/v1/Bills/512/Publications",
                cache=create_json_cache("openapi-tests"),
                notification=TaskNotification(title="ClientTestCase"),
                items_key="publications",
                item_func=item_func,
                items_per_page=1,
                max_items=1,
            )

        self.assertEqual(publication_id, 2716)


class LiveClientTestCase(NetworkTestCase):
    """Clone of ClientTestCase but using live network calls to make sure API format has not changed."""

    def test_client_foreach_with_list_response(self):
        """Test foreach when the endpoint returns an unwrapped list of items."""
        items_processed = 0
        division_id = None

        def item_func(data: dict, _: TaskNotification | None) -> None:
            """Signature: openapi_client.ItemFunc"""
            nonlocal items_processed, division_id
            items_processed += 1
            division_id = data.get("divisionId")

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

        def item_func(data: dict, _: TaskNotification | None) -> None:
            """Signature: openapi_client.ItemFunc"""
            nonlocal items_processed, bill_id
            items_processed += 1
            bill_id = data.get("billId")

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
