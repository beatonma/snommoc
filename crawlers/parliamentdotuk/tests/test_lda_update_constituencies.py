import logging
from unittest import mock

import requests

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda import lda_client
from crawlers.parliamentdotuk.tasks.lda.update_constituencies import (
    update_constituencies,
)
from repository.models import Constituency

log = logging.getLogger(__name__)

EXAMPLE_RESPONSE = { 'format': 'linked-data-api', 'version': '0.2', 'result': { '_about': 'http://eldaddp.azurewebsites.net/constituencies.json', 'definition': 'http://eldaddp.azurewebsites.net/meta/constituencies.json', 'extendedMetadataVersion': 'http://eldaddp.azurewebsites.net/constituencies.json?_metadata=all', 'first': 'http://eldaddp.azurewebsites.net/constituencies.json?_page=0', 'hasPart': 'http://eldaddp.azurewebsites.net/constituencies.json', 'isPartOf': 'http://eldaddp.azurewebsites.net/constituencies.json', 'items': [ { '_about': 'http://data.parliament.uk/resources/143461', 'constituencyType': '', 'endedDate': {'_value': '1950-02-23', '_datatype': 'dateTime'}, 'gssCode': '', 'label': {'_value': 'Aberavon'}, 'osName': '', 'startedDate': {'_value': '1918-12-14', '_datatype': 'dateTime'}, }, { '_about': 'http://data.parliament.uk/resources/143462', 'constituencyType': '', 'endedDate': {'_value': '1974-02-28', '_datatype': 'dateTime'}, 'gssCode': '', 'label': {'_value': 'Aberavon'}, 'osName': '', 'startedDate': {'_value': '1950-02-23', '_datatype': 'dateTime'}, }, { '_about': 'http://data.parliament.uk/resources/143463', 'constituencyType': 'County', 'endedDate': {'_value': '1983-06-09', '_datatype': 'dateTime'}, 'gssCode': '', 'label': {'_value': 'Aberavon'}, 'osName': '', 'startedDate': {'_value': '1974-02-28', '_datatype': 'dateTime'}, }, { '_about': 'http://data.parliament.uk/resources/143464', 'constituencyType': 'County', 'endedDate': {'_value': '1997-05-01', '_datatype': 'dateTime'}, 'gssCode': '', 'label': {'_value': 'Aberavon'}, 'osName': '', 'startedDate': {'_value': '1983-06-09', '_datatype': 'dateTime'}, }, { '_about': 'http://data.parliament.uk/resources/143465', 'constituencyType': 'County', 'endedDate': {'_value': '2010-05-06', '_datatype': 'dateTime'}, 'gssCode': '', 'label': {'_value': 'Aberavon'}, 'osName': 'Aberavon Co Const', 'startedDate': {'_value': '1997-05-01', '_datatype': 'dateTime'}, }, { '_about': 'http://data.parliament.uk/resources/146747', 'constituencyType': 'County', 'gssCode': 'W07000049', 'label': {'_value': 'Aberavon'}, 'osName': '', 'startedDate': {'_value': '2010-05-06', '_datatype': 'dateTime'}, }, { '_about': 'http://data.parliament.uk/resources/146748', 'constituencyType': 'County', 'gssCode': 'W07000058', 'label': {'_value': 'Aberconwy'}, 'osName': 'Aberconwy Co Const', 'startedDate': {'_value': '2010-05-06', '_datatype': 'dateTime'}, }, { '_about': 'http://data.parliament.uk/resources/143466', 'constituencyType': '', 'endedDate': {'_value': '1974-02-28', '_datatype': 'dateTime'}, 'gssCode': '', 'label': {'_value': 'Aberdare'}, 'osName': '', 'startedDate': {'_value': '1950-02-23', '_datatype': 'dateTime'}, }, { '_about': 'http://data.parliament.uk/resources/143467', 'constituencyType': 'Borough', 'endedDate': {'_value': '1983-06-09', '_datatype': 'dateTime'}, 'gssCode': '', 'label': {'_value': 'Aberdare'}, 'osName': '', 'startedDate': {'_value': '1974-02-28', '_datatype': 'dateTime'}, }, { '_about': 'http://data.parliament.uk/resources/143468', 'constituencyType': 'Borough', 'endedDate': {'_value': '2005-05-05', '_datatype': 'dateTime'}, 'gssCode': '', 'label': {'_value': 'Aberdeen Central'}, 'osName': 'Aberdeen Central Burgh Const', 'startedDate': {'_value': '1997-05-01', '_datatype': 'dateTime'}, }, ], 'itemsPerPage': 10, 'next': 'http://eldaddp.azurewebsites.net/constituencies.json?_page=1', 'page': 0, 'startIndex': 1, 'totalResults': 3877, 'type': [ 'http://purl.org/linked-data/api/vocab#ListEndpoint', 'http://purl.org/linked-data/api/vocab#Page', ], }, }


def get_mock_json_response(*args, **kwargs):
    class MockJsonResponse:
        def __init__(self, url, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            print(f'MOCK RESPONSE: {url}')

        def json(self):
            return self.json_data

    return MockJsonResponse(args[0], EXAMPLE_RESPONSE, 200)


class UpdateConstituenciesTest(LocalTestCase):
    """"""

    @mock.patch.object(
        requests, 'get',
        mock.Mock(side_effect=get_mock_json_response),
    )
    @mock.patch.object(
        lda_client, 'get_next_page_url',
        mock.Mock(side_effect=lambda x: None)
    )
    def test_update_constituencies(self):
        self.assertEqual(len(Constituency.objects.all()), 0)
        update_constituencies()
        new_constituencies = Constituency.objects.all()
        self.assertEqual(len(new_constituencies), 2)

        aberavon = new_constituencies.get(name='Aberavon')
        self.assertEqual(aberavon.constituency_type, 'County')
        self.assertEqual(aberavon.gss_code, 'W07000049')
        self.assertEqual(aberavon.ordinance_survey_name, '')

        aberconwy = new_constituencies.get(name='Aberconwy')
        self.assertEqual(aberconwy.constituency_type, 'County')
        self.assertEqual(aberconwy.gss_code, 'W07000058')
        self.assertEqual(aberconwy.ordinance_survey_name, 'Aberconwy Co Const')

    def tearDown(self) -> None:
        Constituency.objects.all().delete()
