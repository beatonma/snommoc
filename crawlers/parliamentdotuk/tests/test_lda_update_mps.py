"""

"""

import logging
from unittest import (
    mock,
    skip,
)

import requests

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda import util as lda_util
from crawlers.parliamentdotuk.tasks.lda.update_mps import update_mps
from repository.models import (
    Constituency,
    Party,
    Mp,
)

log = logging.getLogger(__name__)

EXAMPLE_RESPONSE = {
    "format": "linked-data-api",
    "version": "0.2",
    "result": {
        "_about": "http://eldaddp.azurewebsites.net/commonsmembers.json",
        "definition": "http://eldaddp.azurewebsites.net/meta/commonsmembers.json",
        "extendedMetadataVersion": "http://eldaddp.azurewebsites.net/commonsmembers.json?_metadata=all",
        "first": "http://eldaddp.azurewebsites.net/commonsmembers.json?_page=0",
        "hasPart": "http://eldaddp.azurewebsites.net/commonsmembers.json",
        "isPartOf": "http://eldaddp.azurewebsites.net/commonsmembers.json",
        "items": [
            {
                "_about": "http://data.parliament.uk/members/172",
                "additionalName": {"_value": "Julie"},
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/146966",
                    "label": {"_value": "Hackney North and Stoke Newington"},
                },
                "familyName": {"_value": "Abbott"},
                "fullName": {"_value": "Ms Diane Abbott"},
                "gender": {"_value": "Female"},
                "givenName": {"_value": "Diane"},
                "homePage": "http://www.dianeabbott.org.uk",
                "label": {"_value": "Biography information for Ms Diane Abbott"},
                "party": {"_value": "Labour"},
                "twitter": {"_value": "https://twitter.com/HackneyAbbott"},
            },
            {
                "_about": "http://data.parliament.uk/members/4212",
                "additionalName": {"_value": "Angela Elspeth Marie"},
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/147130",
                    "label": {"_value": "Oldham East and Saddleworth"},
                },
                "familyName": {"_value": "Abrahams"},
                "fullName": {"_value": "Debbie Abrahams"},
                "gender": {"_value": "Female"},
                "givenName": {"_value": "Deborah"},
                "homePage": "http://www.debbieabrahams.org.uk/",
                "label": {"_value": "Biography information for Debbie Abrahams"},
                "party": {"_value": "Labour"},
                "twitter": {"_value": "https://twitter.com/Debbie_abrahams"},
            },
            {
                "_about": "http://data.parliament.uk/members/662",
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/146403",
                    "label": {"_value": "Torfaen"},
                },
                "familyName": {"_value": "Abse"},
                "fullName": {"_value": "Leo Abse"},
                "gender": {"_value": "Male"},
                "givenName": {"_value": "Leopold"},
                "label": {"_value": "Biography information for Leo Abse"},
                "party": {"_value": "Labour"},
            },
            {
                "_about": "http://data.parliament.uk/members/663",
                "additionalName": {"_value": "Steele"},
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/145747",
                    "label": {"_value": "Paisley North"},
                },
                "familyName": {"_value": "Adams"},
                "fullName": {"_value": "Allen Adams"},
                "gender": {"_value": "Male"},
                "givenName": {"_value": "Allender"},
                "label": {"_value": "Biography information for Allen Adams"},
                "party": {"_value": "Labour"},
            },
            {
                "_about": "http://data.parliament.uk/members/645",
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/146777",
                    "label": {"_value": "Belfast West"},
                },
                "familyName": {"_value": "Adams"},
                "fullName": {"_value": "Mr Gerry Adams"},
                "gender": {"_value": "Male"},
                "givenName": {"_value": "Gerard"},
                "label": {"_value": "Biography information for Mr Gerry Adams"},
                "party": {"_value": "Sinn Féin"},
            },
            {
                "_about": "http://data.parliament.uk/members/4057",
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/147180",
                    "label": {"_value": "Selby and Ainsty"},
                },
                "familyName": {"_value": "Adams"},
                "fullName": {"_value": "Nigel Adams"},
                "gender": {"_value": "Male"},
                "givenName": {"_value": "Nigel"},
                "homePage": "http://www.selbyandainsty.com/",
                "label": {"_value": "Biography information for Nigel Adams"},
                "party": {"_value": "Conservative"},
            },
            {
                "_about": "http://data.parliament.uk/members/665",
                "additionalName": {"_value": "James"},
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/144142",
                    "label": {"_value": "Christchurch"},
                },
                "familyName": {"_value": "Adley"},
                "fullName": {"_value": "Robert Adley"},
                "gender": {"_value": "Male"},
                "givenName": {"_value": "Robert"},
                "label": {"_value": "Biography information for Robert Adley"},
                "party": {"_value": "Conservative"},
            },
            {
                "_about": "http://data.parliament.uk/members/4639",
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/146995",
                    "label": {"_value": "Hitchin and Harpenden"},
                },
                "familyName": {"_value": "Afolami"},
                "fullName": {"_value": "Bim Afolami"},
                "gender": {"_value": "Male"},
                "givenName": {"_value": "Abimbola"},
                "label": {"_value": "Biography information for Bim Afolami"},
                "party": {"_value": "Conservative"},
                "twitter": {"_value": "https://twitter.com/BimAfolami"},
            },
            {
                "_about": "http://data.parliament.uk/members/1586",
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/147315",
                    "label": {"_value": "Windsor"},
                },
                "familyName": {"_value": "Afriyie"},
                "fullName": {"_value": "Adam Afriyie"},
                "gender": {"_value": "Male"},
                "givenName": {"_value": "Adam"},
                "homePage": "http://www.adamafriyie.org/",
                "label": {"_value": "Biography information for Adam Afriyie"},
                "party": {"_value": "Conservative"},
                "twitter": {"_value": "https://twitter.com/AdamAfriyie"},
            },
            {
                "_about": "http://data.parliament.uk/members/4427",
                "constituency": {
                    "_about": "http://data.parliament.uk/resources/145694",
                    "label": {"_value": "Ochil and South Perthshire"},
                },
                "familyName": {"_value": "Ahmed-Sheikh"},
                "fullName": {"_value": "Ms Tasmina Ahmed-Sheikh"},
                "gender": {"_value": "Female"},
                "givenName": {"_value": "Tasmina"},
                "label": {
                    "_value": "Biography information for Ms Tasmina Ahmed-Sheikh"
                },
                "party": {"_value": "Scottish National Party"},
                "twitter": {"_value": "https://twitter.com/TasminaSheikh"},
            },
        ],
        "itemsPerPage": 10,
        "next": "http://eldaddp.azurewebsites.net/commonsmembers.json?_page=1",
        "page": 0,
        "startIndex": 1,
        "totalResults": 1962,
        "type": [
            "http://purl.org/linked-data/api/vocab#ListEndpoint",
            "http://purl.org/linked-data/api/vocab#Page",
        ],
    },
}


def get_mock_json_response(*args, **kwargs):
    class MockJsonResponse:
        def __init__(self, url, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            print(f'MOCK RESPONSE: {url}')

        def json(self):
            return self.json_data

    return MockJsonResponse(args[0], EXAMPLE_RESPONSE, 200)


@skip(reason='Not yet implemented')
class UpdateMPsTest(LocalTestCase):
    """"""

    @mock.patch.object(
        requests, 'get',
        mock.Mock(side_effect=get_mock_json_response),
    )
    @mock.patch.object(
        lda_util, 'get_next_page_url',
        mock.Mock(side_effect=lambda x: None),
    )
    def test_update_mps(self):
        self.assertEqual(len(Mp.objects.all()), 0)
        update_mps()
        new_mps = Mp.objects.all()

    def tearDown(self) -> None:
        Constituency.objects.all().delete()
        Party.objects.all().delete()
        Mp.objects.all().delete()

# inject_context_manager(CommonsMember)
#
#
# class TestCommonsMemberParsing(LocalTestCase):
#     """"""
#
#     def test_create_members(self):
#         members = create_members(EXAMPLE_MEMBER_JSON_ITEMS)
#
#         with members[0] as member:
#             self.assertEqual(member.family_name, "Abbott")
#             self.assertEqual(member.given_name, "Diane")
#             self.assertEqual(member.gender, "Female")
#             self.assertEqual(member.home_page, "http://www.dianeabbott.org.uk")
#             self.assertEqual(member.party, "Labour")
#             self.assertEqual(member.twitter, "https://twitter.com/HackneyAbbott")
#             self.assertEqual(member.constituency, "Hackney North and Stoke Newington")
#
#         with members[1] as member:
#             self.assertEqual(member.family_name, "Abrahams")
#             self.assertEqual(member.given_name, "Deborah")
#             self.assertEqual(member.gender, "Female")
#             self.assertEqual(member.home_page, "http://www.debbieabrahams.org.uk/")
#             self.assertEqual(member.party, "Labour")
#             self.assertEqual(member.twitter, "https://twitter.com/Debbie_abrahams")
#             self.assertEqual(member.constituency, "Oldham East and Saddleworth")