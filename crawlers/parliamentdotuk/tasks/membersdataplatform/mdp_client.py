"""

"""
import datetime
import logging
import uuid
from typing import (
    Callable,
    List,
    Optional,
    Tuple,
    Type,
)

import dateutil
import requests
from dateutil.parser import ParserError
from django.conf import settings

from notifications.models import TaskNotification
from .contract import (
    basic_details as basic_contract,
    constituencies as constituencies_contract,
    houses as houses_contract,
    maiden_speeches as speech_contract,
    member as member_contract,
    party as party_contract,
    status as status_contract,
    committees as committee_contract,
)

log = logging.getLogger(__name__)

"""
Get addresses (physical/internets) for all members of a house: http://data.parliament.uk/membersdataplatform/services/mnis/members/query/house=Lords/Addresses/
Get MP status: http://data.parliament.uk/membersdataplatform/services/mnis/members/query/house=Commons/Statuses/
"""


def get(url: str):
    """Get the url using our standard headers and fix response encoding."""
    response = requests.get(url, headers=settings.HTTP_REQUEST_HEADERS)
    response.encoding = 'utf-8-sig'
    return response


def _coerce_to_list(obj) -> list:
    """Wrap the given object in a list if it is not already a list.

    Some API responses return a list or a single object. To avoid handling each
    case separately we use this function to make sure we always have a list.
    """
    if obj is None:
        return []
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]


def _coerce_to_date(value) -> Optional[datetime.date]:
    try:
        return dateutil.parser.parse(value).date()
    except (AttributeError, TypeError, ParserError):
        return None


def _coerce_to_str(value) -> Optional[str]:
    return str(value) if value else None


def _coerce_to_int(value) -> Optional[int]:
    try:
        return int(value)
    except ValueError:
        return None


def _coerce_to_boolean(value) -> Optional[bool]:
    if value is None:
        return None

    if isinstance(value, str):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False

    return bool(value)


def _is_xml_null(obj: dict) -> bool:
    """Some values return an xml-schema-wrapped version of null.

    Return True iff the given object is an instance of xml-wrapped null.
    """
    return isinstance(obj, dict) and obj.get('@xsi:nil', '').lower() == 'true'


def _get_nested_value(obj: dict, key: str):
    parts = key.split('.')
    parent = obj
    while len(parts) > 1:
        parent = parent.get(parts.pop(0))
        if parent is None or not isinstance(parent, dict):
            log.warning(f'Nested key \'{key}\' not accessible in this object')
            return None

    result = parent.get(parts.pop())
    if _is_xml_null(result):
        return None
    return result


class ResponseData:
    def __init__(self, json_data: dict):
        self.data = json_data

    def get_value(self, key: str):
        """Nested values may be accessed by inserting a dot between nested keys.

        e.g. get_value('top.middle.bottom') -> top.get('middle').get('bottom')"""
        if '.' in key:
            return _get_nested_value(self.data, key)

        result = self.data.get(key)
        if _is_xml_null(result):
            return None
        if isinstance(result, str):
            result = result.strip()
        return result

    def _get_list(self, key: str) -> List:
        return _coerce_to_list(self.get_value(key))

    def _get_str(self, key: str) -> Optional[str]:
        return _coerce_to_str(self.get_value(key))

    def _get_int(self, key: str) -> Optional[int]:
        return _coerce_to_int(self.get_value(key))

    def _get_boolean(self, key: str) -> Optional[bool]:
        return _coerce_to_boolean(self.get_value(key))

    def _get_date(self, key: str) -> Optional[datetime.date]:
        return _coerce_to_date(self.get_value(key))

    def _get_response_list(self, key, response_class: Type):
        objects = self._get_list(key)
        return [response_class(o) for o in objects]


class MemberResponseData(ResponseData):

    def get_parliament_id(self) -> int:
        return self._get_int(member_contract.MEMBER_ID)

    def get_name(self) -> Optional[str]:
        return self._get_str(member_contract.DISPLAY_NAME)

    def get_full_title(self) -> Optional[str]:
        return self._get_str(member_contract.FULL_TITLE)

    def get_gender(self) -> Optional[str]:
        return self._get_str(member_contract.GENDER)

    def get_constituency(self) -> Optional[str]:
        return self._get_str(member_contract.MEMBER_FROM)

    def get_house(self) -> Optional[str]:
        return self._get_str(member_contract.HOUSE)

    def get_date_of_birth(self) -> Optional[datetime.date]:
        return self._get_date(member_contract.DATE_OF_BIRTH)

    def get_date_of_death(self) -> Optional[datetime.date]:
        return self._get_date(member_contract.DATE_OF_DEATH)

    def get_house_start_date(self) -> Optional[datetime.date]:
        return self._get_date(member_contract.DATE_HOUSE_ENTERED)

    def get_house_end_date(self) -> Optional[datetime.date]:
        return self._get_date(member_contract.DATE_HOUSE_LEFT)

    def get_party(self) -> Optional[str]:
        return self._get_str(f'{member_contract.PARTY}.{member_contract.PARTY_NAME}')

    def get_is_active(self) -> bool:
        return self._get_boolean(f'{status_contract.CURRENT_STATUS}.{status_contract.IS_ACTIVE}')


class BasicInfoResponseData(ResponseData):
    def get_family_name(self) -> Optional[str]:
        return self._get_str(basic_contract.SURNAME)

    def get_first_name(self) -> Optional[str]:
        return self._get_str(basic_contract.FORENAME)

    def get_middle_names(self) -> Optional[str]:
        return self._get_str(basic_contract.MIDDLE_NAMES)

    def get_town_of_birth(self) -> Optional[str]:
        return self._get_str(basic_contract.TOWN_OF_BIRTH)

    def get_country_of_birth(self) -> Optional[str]:
        return self._get_str(basic_contract.COUNTRY_OF_BIRTH)


class ConstituencyResponseData(ResponseData):
    def _get_election_value(self, key: str):
        return self.get_value(f'{constituencies_contract.ELECTION}.{key}')

    def get_constituency_id(self) -> Optional[int]:
        return self._get_int(constituencies_contract.PARLIAMENTDOTUK)

    def get_constituency_name(self) -> Optional[str]:
        return self._get_str(constituencies_contract.NAME)

    def get_start_date(self) -> datetime.date:
        return self._get_date(constituencies_contract.START_DATE)

    def get_end_date(self) -> datetime.date:
        return self._get_date(constituencies_contract.END_DATE)

    def get_election_id(self) -> Optional[int]:
        return _coerce_to_int(self._get_election_value(constituencies_contract.PARLIAMENTDOTUK))

    def get_election_name(self) -> str:
        return _coerce_to_str(self._get_election_value(constituencies_contract.NAME))

    def get_election_date(self) -> datetime.date:
        return _coerce_to_date(self._get_election_value(constituencies_contract.ELECTION_DATE))


class PartyResponseData(ResponseData):
    def get_party_name(self) -> Optional[str]:
        return self._get_str(party_contract.PARTY_NAME)

    def get_start_date(self) -> Optional[datetime.date]:
        return self._get_date(party_contract.START_DATE)

    def get_end_date(self) -> Optional[datetime.date]:
        return self._get_date(party_contract.END_DATE)


class HouseMembershipResponseData(ResponseData):
    def get_house(self) -> Optional[str]:
        return self._get_str(houses_contract.HOUSE)

    def get_start_date(self) -> datetime.date:
        return self._get_date(houses_contract.START_DATE)

    def get_end_date(self) -> Optional[datetime.date]:
        return self._get_date(houses_contract.END_DATE)


class SpeechResponseData(ResponseData):
    def get_house(self) -> Optional[str]:
        return self._get_str(speech_contract.HOUSE)

    def get_date(self) -> Optional[datetime.date]:
        return self._get_date(speech_contract.DATE)

    def get_subject(self) -> Optional[str]:
        return self._get_str(speech_contract.SUBJECT)

    def get_hansard(self) -> Optional[str]:
        return self._get_str(speech_contract.HANSARD)


class CommitteeResponseData(ResponseData):
    def get_committee_id(self) -> Optional[int]:
        return self._get_int(committee_contract.PARLIAMENTDOTUK)

    def get_committee_name(self) -> Optional[str]:
        return self._get_str(committee_contract.NAME)

    def get_start_date(self) -> Optional[datetime.date]:
        return self._get_date(committee_contract.START_DATE)

    def get_end_date(self) -> Optional[datetime.date]:
        return self._get_date(committee_contract.END_DATE)

    def get_chair(self) -> List['CommitteeChairResponseData']:
        return self._get_response_list(committee_contract.CHAIR_GROUP_KEY, CommitteeChairResponseData)


class CommitteeChairResponseData(ResponseData):
    def get_start_date(self) -> Optional[datetime.date]:
        return self._get_date(committee_contract.START_DATE)

    def get_end_date(self) -> Optional[datetime.date]:
        return self._get_date(committee_contract.END_DATE)


class MemberBiographyResponseData(MemberResponseData):
    def get_basic_info(self) -> 'BasicInfoResponseData':
        return BasicInfoResponseData(self.get_value(basic_contract.BASIC_DETAILS))

    def get_house_memberships(self) -> List['HouseMembershipResponseData']:
        return self._get_response_list(houses_contract.GROUP_KEY, HouseMembershipResponseData)

    def get_constituencies(self) -> List['ConstituencyResponseData']:
        return self._get_response_list(constituencies_contract.GROUP_KEY, ConstituencyResponseData)

    def get_parties(self) -> List['PartyResponseData']:
        return self._get_response_list(party_contract.GROUP_KEY, PartyResponseData)

    def get_maiden_speeches(self) -> List['SpeechResponseData']:
        return self._get_response_list(speech_contract.GROUP_KEY, SpeechResponseData)


def update_members(
        endpoint_url: str,
        update_member_func: Callable[[Type[ResponseData]], Optional[str]],
        report_func: Optional[Callable[[List[str]], Tuple[str, str]]],
        response_class=MemberResponseData,
) -> None:
    update_id = uuid.uuid4().hex[:6]
    new_members: List[str] = []
    TaskNotification.objects.create(
        title=f'Task started [id={update_id}]',
        content=f'An update cycle has started for endpoint {endpoint_url}'
    ).save()

    response = get(endpoint_url)
    try:
        data = response.json()
        members = data.get('Members').get('Member')

        if not isinstance(members, list):
            members = [members]

    except AttributeError as e:
        log.warning(f'Could not read item list: {e}')
        TaskNotification.objects.create(
            title=f'Task failed [id={update_id}]',
            content=f'Update failed for endpoint {endpoint_url}: {e}'
        ).save()
        return

    for member in members:
        new_name = update_member_func(response_class(member))
        if new_name:
            new_members.append(new_name)

    if report_func:
        title, content = report_func(new_members)
        TaskNotification.objects.create(
            title=f'[id={update_id} finished] {title}',
            content=content
        ).save()
