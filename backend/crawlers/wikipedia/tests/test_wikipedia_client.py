from unittest.mock import patch

from basetest.testcase import LocalTestCase
from crawlers.context import TaskContext
from crawlers.wikipedia import wikipedia_client
from crawlers.wikipedia.tasks import schema
from notifications.models import TaskNotification

CONTEXT = TaskContext(None, TaskNotification())

_SAMPLE = {
    "batchcomplete": "",
    "query": {
        "normalized": [{"from": "Boris_Johnson", "to": "Boris Johnson"}],
        "pages": {
            "18681487": {
                "pageid": 18681487,
                "ns": 0,
                "title": "Keir Starmer",
                "thumbnail": {
                    "source": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Official_portrait_of_Keir_Starmer_crop_2.jpg/75px-Official_portrait_of_Keir_Starmer_crop_2.jpg",
                    "width": 75,
                    "height": 100,
                },
                "pageimage": "Official_portrait_of_Keir_Starmer_crop_2.jpg",
            },
            "19065069": {
                "pageid": 19065304,
                "ns": 0,
                "title": "Boris Johnson",
                "thumbnail": {
                    "source": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Boris_Johnson_official_portrait_%28cropped%29.jpg/71px-Boris_Johnson_official_portrait_%28cropped%29.jpg",
                    "width": 71,
                    "height": 100,
                },
                "pageimage": "Boris_Johnson_official_portrait_(cropped).jpg",
            },
        },
    },
}


def _patch():
    return patch(
        "crawlers.wikipedia.wikipedia_client.get_json",
        side_effect=lambda *a, **kw: _SAMPLE,
    )


class WikipediaClientTests(LocalTestCase):
    """"""

    def test_for_pages(self):
        results = {}

        with _patch():

            def _block(t, x):
                results[t] = x.pageid

            wikipedia_client.for_each_page(
                ["Boris_Johnson", "Keir Starmer"],
                block=_block,
                page_class=schema.Page,
                context=CONTEXT,
                prop="pageimages",
            )

        self.assertDictEqual(
            results,
            {
                "Boris_Johnson": 19065304,
                "Keir Starmer": 18681487,
            },
        )
