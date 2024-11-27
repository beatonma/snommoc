from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks.openapi import openapi_client
from crawlers.parliamentdotuk.tasks.openapi.testcase import OpenApiTestCase
from notifications.models import TaskNotification

TASK_CONTEXT = TaskContext(
    None,
    TaskNotification(title="ClientTestCase"),
    max_items=1,
    items_per_page=1,
)


class ClientTestCase(OpenApiTestCase):
    file = __file__
    mock_response = {
        "https://bills-api.parliament.uk/api/v1/Bills/512/Publications": "data/response_custom_items_key.json",
        "https://lordsvotes-api.parliament.uk/data/Divisions/search": "data/response_list.json",
        "https://bills-api.parliament.uk/api/v1/Bills": "data/response_default_items_key.json",
    }

    def test_client_foreach_with_list_response(self):
        """Test foreach when the endpoint returns an unwrapped list of items."""
        items_processed = 0
        division_id = None

        def item_func(data: dict, _: TaskContext) -> None:
            """Signature: openapi_client.ItemFunc"""
            nonlocal items_processed, division_id
            items_processed += 1
            division_id = data.get("divisionId")

        with self.patch():
            openapi_client.foreach(
                "https://lordsvotes-api.parliament.uk/data/Divisions/search",
                context=TASK_CONTEXT,
                item_func=item_func,
            )

        self.assertEqual(items_processed, 1)
        self.assertEqual(division_id, 2684)

    def test_client_foreach_with_wrapped_response(self):
        """Test foreach when the endpoint returns a dictionary with an 'items' child list."""
        items_processed = 0
        bill_id = None

        def item_func(data: dict, _: TaskContext) -> None:
            nonlocal items_processed, bill_id
            items_processed += 1
            bill_id = data.get("billId")

        with self.patch():
            openapi_client.foreach(
                "https://bills-api.parliament.uk/api/v1/Bills",
                context=TASK_CONTEXT,
                item_func=item_func,
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

        with self.patch():
            openapi_client.foreach(
                "https://bills-api.parliament.uk/api/v1/Bills/512/Publications",
                context=TASK_CONTEXT,
                items_key="publications",
                item_func=item_func,
            )

        self.assertEqual(publication_id, 2716)
