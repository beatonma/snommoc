from basetest.testcase import SimpleTestCase
from crawlers.network.network import _resolve_query


class GetJsonTest(SimpleTestCase):
    def test_resolve_query(self):
        url, params = _resolve_query(
            "https://bills-api.parliament.uk/api/v1/Bills?SortOrder=DateUpdatedDescending",
            {"skip": 0, "take": 2},
        )
        self.assertEqual(url, "https://bills-api.parliament.uk/api/v1/Bills")
        self.assertDictEqual(
            params, {"skip": 0, "take": 2, "SortOrder": "DateUpdatedDescending"}
        )

    def test_params_override_url(self):
        url, params = _resolve_query(
            "https://bills-api.parliament.uk/api/v1/Bills?SortOrder=DateUpdatedDescending",
            {"skip": 0, "take": 2, "SortOrder": "TitleDescending"},
        )
        self.assertEqual(url, "https://bills-api.parliament.uk/api/v1/Bills")
        self.assertDictEqual(
            params,
            {
                "skip": 0,
                "take": 2,
                "SortOrder": "TitleDescending",  # Value from `params` overrules that given in the url
            },
        )
