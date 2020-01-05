"""

"""
import datetime
import logging
from unittest import mock

import requests

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import (
    MemberResponseData,
    ResponseData,
)
from crawlers.parliamentdotuk.tasks.membersdataplatform.all_members import (
    _update_member_basic_info,
    update_all_mps_basic_info,
)
from repository.models.person import Person

log = logging.getLogger(__name__)

EXAMPLE_JSON_SINGLE_MP = {"@Member_Id": "172", "@Dods_Id": "25790", "@Pims_Id": "3572", "@Clerks_Id": "1", "DisplayAs": "Ms Diane Abbott", "ListAs": "Abbott, Ms Diane", "FullTitle": "Rt Hon Diane Abbott MP", "LayingMinisterName": None, "DateOfBirth": "1953-09-27T00:00:00", "DateOfDeath": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Gender": "F", "Party": {"@Id": "15", "#text": "Labour"}, "House": "Commons", "MemberFrom": "Hackney North and Stoke Newington", "HouseStartDate": "1987-06-11T00:00:00", "HouseEndDate": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "CurrentStatus": {"@Id": "0", "@IsActive": "True", "Name": "Current Member", "Reason": None, "StartDate": "2019-12-12T00:00:00"}}
EXAMPLE_RESPONSE_SINGLE_MP = {"Members":{"Member":{"@Member_Id":"172","@Dods_Id":"25790","@Pims_Id":"3572","@Clerks_Id":"1","DisplayAs":"Ms Diane Abbott","ListAs":"Abbott, Ms Diane","FullTitle":"Rt Hon Diane Abbott MP","LayingMinisterName":None,"DateOfBirth":"1953-09-27T00:00:00","DateOfDeath":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"Gender":"F","Party":{"@Id":"15","#text":"Labour"},"House":"Commons","MemberFrom":"Hackney North and Stoke Newington","HouseStartDate":"1987-06-11T00:00:00","HouseEndDate":{"@xsi:nil":"true","@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"},"CurrentStatus":{"@Id":"0","@IsActive":"True","Name":"Current Member","Reason":None,"StartDate":"2019-12-12T00:00:00"},"Interests":None}}}
EXAMPLE_RESPONSE_MANY_MPS ={"Members": {"Member": [{"@Member_Id": "172", "@Dods_Id": "25790", "@Pims_Id": "3572", "@Clerks_Id": "1", "DisplayAs": "Ms Diane Abbott", "ListAs": "Abbott, Ms Diane", "FullTitle": "Rt Hon Diane Abbott MP", "LayingMinisterName": None, "DateOfBirth": "1953-09-27T00:00:00", "DateOfDeath": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Gender": "F", "Party": {"@Id": "15", "#text": "Labour"}, "House": "Commons", "MemberFrom": "Hackney North and Stoke Newington", "HouseStartDate": "1987-06-11T00:00:00", "HouseEndDate": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "CurrentStatus": {"@Id": "0", "@IsActive": "True", "Name": "Current Member", "Reason": None, "StartDate": "2019-12-12T00:00:00"}}, {"@Member_Id": "4212", "@Dods_Id": "80556", "@Pims_Id": "5905", "@Clerks_Id": "5905", "DisplayAs": "Debbie Abrahams", "ListAs": "Abrahams, Debbie", "FullTitle": "Debbie Abrahams MP", "LayingMinisterName": None, "DateOfBirth": "1960-09-15T00:00:00", "DateOfDeath": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "Gender": "F", "Party": {"@Id": "15", "#text": "Labour"}, "House": "Commons", "MemberFrom": "Oldham East and Saddleworth", "HouseStartDate": "2011-01-13T00:00:00", "HouseEndDate": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}, "CurrentStatus": {"@Id": "0", "@IsActive": "True", "Name": "Current Member", "Reason": None, "StartDate": "2019-12-12T00:00:00"}}, {"@Member_Id": "662", "@Dods_Id": "", "@Pims_Id": "", "@Clerks_Id": "", "DisplayAs": "Leo Abse", "ListAs": "Abse, Leo", "FullTitle": "Leo Abse", "LayingMinisterName": None, "DateOfBirth": "1917-04-22T00:00:00", "DateOfDeath": "2008-08-19T00:00:00", "Gender": "M", "Party": {"@Id": "15", "#text": "Labour"}, "House": "Commons", "MemberFrom": "Torfaen", "HouseStartDate": "1958-11-10T00:00:00", "HouseEndDate": "1987-06-11T00:00:00", "CurrentStatus": {"@Id": "", "@IsActive": "False", "Name": None, "Reason": None, "StartDate": {"@xsi:nil": "true", "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}}}]}}


def get_mock_json_response_single_mp(*args, **kwargs):
    class MockJsonResponse:
        def __init__(self, url, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            print(f'MOCK RESPONSE: {url}')

        def json(self):
            return self.json_data

    return MockJsonResponse(args[0], EXAMPLE_RESPONSE_SINGLE_MP, 200)


def get_mock_json_response_many_mps(*args, **kwargs):
    class MockJsonResponse:
        def __init__(self, url, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            print(f'MOCK RESPONSE: {url}')

        def json(self):
            return self.json_data

    return MockJsonResponse(args[0], EXAMPLE_RESPONSE_MANY_MPS, 200)


class ResponseDataTest(LocalTestCase):
    """Ensure that the ResponseData class exposes json properties correctly."""
    def test_nested_get_value(self):
        responsedata = ResponseData(EXAMPLE_JSON_SINGLE_MP)

        self.assertEquals(responsedata._get_value('@Member_Id'), '172')
        self.assertEquals(responsedata._get_value('Party.#text'), 'Labour')
        self.assertEquals(responsedata._get_value('CurrentStatus.StartDate'), "2019-12-12T00:00:00")
        self.assertIsNone(responsedata._get_value('DateOfDeath'))
        self.assertIsNone(responsedata._get_value('CurrentStatus.Reason'))
        self.assertIsNone(responsedata._get_value('Some nonsense'))
        self.assertIsNone(responsedata._get_value('.'))
        self.assertIsNone(responsedata._get_value('.....'))
        self.assertIsNone(responsedata._get_value(''))


class MdpUpdateMpsTest(LocalTestCase):
    """Ensure that basic info is retrieved from API response correctly."""

    def _assert_values_for_diane_abbott(self, ms_abbott: Person):
        """Diane Abbott is currently the first result in most API calls so
        her results are the most easily accessible and useful for testing
        against.
        """
        self.assertEqualIgnoreCase(ms_abbott.name, 'Ms Diane Abbott')
        self.assertEqualIgnoreCase(ms_abbott.full_title, 'Rt Hon Diane Abbott MP')
        self.assertEqualIgnoreCase(ms_abbott.party.name, 'Labour')
        self.assertEqualIgnoreCase(ms_abbott.constituency.name, 'Hackney North and Stoke Newington')
        self.assertEqualIgnoreCase(ms_abbott.house.name, 'Commons')
        self.assertEqual(ms_abbott.date_of_birth, datetime.date(year=1953, month=9, day=27))
        self.assertEqual(ms_abbott.date_entered_house, datetime.date(year=1987, month=6, day=11))
        self.assertIsNone(ms_abbott.date_of_death)
        self.assertIsNone(ms_abbott.date_left_house)

    @mock.patch.object(
        requests, 'get',
        mock.Mock(side_effect=get_mock_json_response_single_mp),
    )
    def test_mdp_client_update_members__wraps_individual_result_in_list(self):
        """The MDP API returns single values as an object,
        not a single-item list, so we wrap it ourselves.
        This test makes sure that that works correctly.
        """
        self.assertEqual(len(Person.objects.all()), 0)

        update_all_mps_basic_info()

        people = Person.objects.all()
        self.assertEqual(len(people), 1)
        self._assert_values_for_diane_abbott(people.first())

    @mock.patch.object(
        requests, 'get',
        mock.Mock(side_effect=get_mock_json_response_many_mps),
    )
    def test_update_all_mps_basic_info(self):
        self.assertEqual(len(Person.objects.all()), 0)

        update_all_mps_basic_info()

        people = Person.objects.all()
        print(people)

        self.assertEquals(len(people), 3)
        diane_abbot: Person = people.get(parliamentdotuk=172)
        self._assert_values_for_diane_abbott(diane_abbot)

        debbie_abrahams: Person = people.get(parliamentdotuk=4212)
        self.assertEqualIgnoreCase(debbie_abrahams.name, 'Debbie Abrahams')
        self.assertTrue(debbie_abrahams.active)

        leo_abse: Person = people.get(parliamentdotuk=662)
        self.assertEqualIgnoreCase(leo_abse.name, 'Leo Abse')
        self.assertFalse(leo_abse.active)

    def test__update_mp_basic_info(self):
        # Make sure person does not exist before update operation
        get_person_func = Person.objects.get
        get_person_kwargs = {
            'parliamentdotuk': 172,
        }
        self.assertRaises(Person.DoesNotExist, get_person_func, **get_person_kwargs)

        _update_member_basic_info(MemberResponseData(EXAMPLE_JSON_SINGLE_MP))

        person = get_person_func(**get_person_kwargs)

        self._assert_values_for_diane_abbott(person)
