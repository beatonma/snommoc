import datetime

from basetest.testcase import (
    LocalTestCase,
    NetworkTestCase,
)
from crawlers.parliamentdotuk.tasks.lda import lda_client
from crawlers.parliamentdotuk.tasks.lda.contract import (
    constituencies as constituencies_contract,
)

EXAMPLE_RESPONSE = {
    "format": "linked-data-api",
    "version": "0.2",
    "result": {
        "_about": "http://eldaddp.azurewebsites.net/constituencies.json",
        "definition": "http://eldaddp.azurewebsites.net/meta/constituencies.json",
        "extendedMetadataVersion": "http://eldaddp.azurewebsites.net/constituencies.json?_metadata=all",
        "first": "http://eldaddp.azurewebsites.net/constituencies.json?_page=0",
        "hasPart": "http://eldaddp.azurewebsites.net/constituencies.json",
        "isPartOf": "http://eldaddp.azurewebsites.net/constituencies.json",
        "items": [
            {
                "_about": "http://data.parliament.uk/resources/143461",
                "constituencyType": "",
                "endedDate": {"_value": "1950-02-23", "_datatype": "dateTime"},
                "gssCode": "",
                "label": {"_value": "Aberavon"},
                "osName": "",
                "startedDate": {"_value": "1918-12-14", "_datatype": "dateTime"},
            },
            {
                "_about": "http://data.parliament.uk/resources/143462",
                "constituencyType": "",
                "endedDate": {"_value": "1974-02-28", "_datatype": "dateTime"},
                "gssCode": "",
                "label": {"_value": "Aberavon"},
                "osName": "",
                "startedDate": {"_value": "1950-02-23", "_datatype": "dateTime"},
            },
            {
                "_about": "http://data.parliament.uk/resources/143463",
                "constituencyType": "County",
                "endedDate": {"_value": "1983-06-09", "_datatype": "dateTime"},
                "gssCode": "",
                "label": {"_value": "Aberavon"},
                "osName": "",
                "startedDate": {"_value": "1974-02-28", "_datatype": "dateTime"},
            },
            {
                "_about": "http://data.parliament.uk/resources/143464",
                "constituencyType": "County",
                "endedDate": {"_value": "1997-05-01", "_datatype": "dateTime"},
                "gssCode": "",
                "label": {"_value": "Aberavon"},
                "osName": "",
                "startedDate": {"_value": "1983-06-09", "_datatype": "dateTime"},
            },
            {
                "_about": "http://data.parliament.uk/resources/143465",
                "constituencyType": "County",
                "endedDate": {"_value": "2010-05-06", "_datatype": "dateTime"},
                "gssCode": "",
                "label": {"_value": "Aberavon"},
                "osName": "Aberavon Co Const",
                "startedDate": {"_value": "1997-05-01", "_datatype": "dateTime"},
            },
            {
                "_about": "http://data.parliament.uk/resources/146747",
                "constituencyType": "County",
                "gssCode": "W07000049",
                "label": {"_value": "Aberavon"},
                "osName": "",
                "startedDate": {"_value": "2010-05-06", "_datatype": "dateTime"},
            },
            {
                "_about": "http://data.parliament.uk/resources/146748",
                "constituencyType": "County",
                "gssCode": "W07000058",
                "label": {"_value": "Aberconwy"},
                "osName": "Aberconwy Co Const",
                "startedDate": {"_value": "2010-05-06", "_datatype": "dateTime"},
            },
            {
                "_about": "http://data.parliament.uk/resources/143466",
                "constituencyType": "",
                "endedDate": {"_value": "1974-02-28", "_datatype": "dateTime"},
                "gssCode": "",
                "label": {"_value": "Aberdare"},
                "osName": "",
                "startedDate": {"_value": "1950-02-23", "_datatype": "dateTime"},
            },
            {
                "_about": "http://data.parliament.uk/resources/143467",
                "constituencyType": "Borough",
                "endedDate": {"_value": "1983-06-09", "_datatype": "dateTime"},
                "gssCode": "",
                "label": {"_value": "Aberdare"},
                "osName": "",
                "startedDate": {"_value": "1974-02-28", "_datatype": "dateTime"},
            },
            {
                "_about": "http://data.parliament.uk/resources/143468",
                "constituencyType": "Borough",
                "endedDate": {"_value": "2005-05-05", "_datatype": "dateTime"},
                "gssCode": "",
                "label": {"_value": "Aberdeen Central"},
                "osName": "Aberdeen Central Burgh Const",
                "startedDate": {"_value": "1997-05-01", "_datatype": "dateTime"},
            },
        ],
        "itemsPerPage": 10,
        "next": "http://eldaddp.azurewebsites.net/constituencies.json?_page=1",
        "page": 0,
        "startIndex": 1,
        "totalResults": 3877,
        "type": [
            "http://purl.org/linked-data/api/vocab#ListEndpoint",
            "http://purl.org/linked-data/api/vocab#Page",
        ],
    },
}
EXAMPLE_ITEM = {
    "_about": "http://data.parliament.uk/resources/146747",
    "constituencyType": "County",
    "gssCode": "W07000049",
    "label": {"_value": "Aberavon"},
    "osName": "",
    "startedDate": {"_value": "2010-05-06", "_datatype": "dateTime"},
}


class LdaClientTests(LocalTestCase):
    """
    lda_client helper function tests.
    """

    def test_get_next_page_url(self):
        next_page_url = lda_client._get_next_page_url(EXAMPLE_RESPONSE)
        self.assertEqual(
            next_page_url,
            "http://eldaddp.azurewebsites.net/constituencies.json?_page=1",
        )

    def test_get_parliamentdotuk_id(self):
        parliamentdotuk = lda_client.get_parliamentdotuk_id(EXAMPLE_ITEM)
        self.assertEqual(parliamentdotuk, 146747)

    def test_get_value(self):
        name = lda_client.get_value(EXAMPLE_ITEM, constituencies_contract.NAME)
        self.assertEqual(name, "Aberavon")

        started_date = lda_client.get_value(
            EXAMPLE_ITEM, constituencies_contract.DATE_STARTED
        )
        self.assertEqual(started_date, "2010-05-06")

    def test_get_date(self):
        started_date = lda_client.get_date(
            EXAMPLE_ITEM, constituencies_contract.DATE_STARTED
        )
        self.assertEqual(started_date, datetime.date(year=2010, month=5, day=6))


class LdaRemoteClientTests(NetworkTestCase):
    """Ensure lda.data.parliament.uk responses are correct"""

    def test_get_page(self):
        page_number = 1
        items_per_page = 15

        data = lda_client._get_list_page_json(
            "http://lda.data.parliament.uk/constituencies.json",
            page_number=page_number,
            page_size=items_per_page,
        )

        result = data.get("result")
        self.assertEqual(result.get("itemsPerPage"), items_per_page)
        self.assertEqual(result.get("page"), page_number)
        self.assertEqual(len(result.get("items")), items_per_page)
