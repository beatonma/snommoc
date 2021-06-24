from unittest.mock import patch

from basetest.testcase import LocalTestCase
from crawlers.wikipedia import wikipedia_client

SAMPLE = {
    "batchcomplete": "",
    "query": {
        "normalized": [{"from": "Boris_Johnson", "to": "Boris Johnson"}],
        "pages": {
            "18681491": {
                "pageid": 18681491,
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
                "pageid": 19065069,
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


class WikipediaClientTests(LocalTestCase):
    """"""

    def test_for_pages(self):
        results = {}

        with patch(
            "crawlers.wikipedia.wikipedia_client._get_wikipedia_api",
            side_effect=lambda *a, **kw: SAMPLE,
        ) as mock_get_wikipedia_api:
            print(mock_get_wikipedia_api())
            mock_get_wikipedia_api.return_value = SAMPLE

            def _block(t, x):
                print("_block", t)
                results[t] = x["pageid"]

            wikipedia_client.for_pages(
                ["Boris_Johnson", "Keir Starmer"],
                block=_block,
                prop="pageimages",
            )

        self.assertDictEqual(
            results,
            {
                "Boris_Johnson": 19065069,
                "Keir Starmer": 18681491,
            },
        )

    def test_get_for_pages(self):
        with patch(
            "crawlers.wikipedia.wikipedia_client._get_wikipedia_api",
            side_effect=lambda *a, **kw: SAMPLE,
        ) as mock_get_wikipedia_api:
            print(mock_get_wikipedia_api())
            mock_get_wikipedia_api.return_value = SAMPLE

            def _block(t, x):
                return (t, x["pageid"])

            results = list(
                wikipedia_client.get_for_pages(
                    ["Boris_Johnson", "Keir Starmer"],
                    block=_block,
                    prop="pageimages",
                )
            )

            self.assertContentsEqual(
                results,
                [
                    ("Boris_Johnson", 19065069),
                    ("Keir Starmer", 18681491),
                ],
            )
