"""

"""
import datetime
import logging
import time
from typing import (
    Callable,
    List,
    Optional,
    Type,
)

import requests
from django.conf import settings

from notifications.models import TaskNotification
from .contract import (
    addresses as address_contract,
    basic_details as basic_contract,
    biography_entries as bio_entries_contract,
    committees as committee_contract,
    constituencies as constituencies_contract,
    election as election_contract,
    elections_contested as contested_contract,
    experience as experience_contract,
    houses as houses_contract,
    interests as interests_contract,
    maiden_speeches as speech_contract,
    member as member_contract,
    party as party_contract,
    posts as posts_contract,
    status as status_contract,
)
from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_list,
    coerce_to_str,
    coerce_to_int,
    coerce_to_boolean,
    coerce_to_date,
)
from .mdp_cache import JsonResponseCache

log = logging.getLogger(__name__)

"""
Get addresses (physical/internets) for all members of a house: http://data.parliament.uk/membersdataplatform/services/mnis/members/query/house=Lords/Addresses/
Get MP status: http://data.parliament.uk/membersdataplatform/services/mnis/members/query/house=Commons/Statuses/
"""


def get(url: str):
    """Get the url using our standard headers and fix response encoding."""
    response = requests.get(url, headers=settings.HTTP_REQUEST_HEADERS_JSON)
    response.encoding = "utf-8-sig"

    time.sleep(1)
    return response


def get_json(url: str, using_cache: Optional[JsonResponseCache] = None) -> dict:
    if using_cache:
        return get_json_with_cache(url, cache=using_cache)

    return get(url).json()


def get_json_with_cache(url: str, cache: JsonResponseCache) -> dict:
    cached = cache.get_json(url)
    if cached:
        return cached

    else:
        data = get(url).json()
        cache.remember(url, data)
        return data


def _is_xml_null(obj: dict) -> bool:
    """Some values return an xml-schema-wrapped version of null.

    Return True iff the given object is an instance of xml-wrapped null.
    """
    return isinstance(obj, dict) and obj.get("@xsi:nil", "").lower() == "true"


def _get_nested_value(obj: dict, key: str):
    parts = key.split(".")
    parent = obj
    while len(parts) > 1:
        parent = parent.get(parts.pop(0))
        if parent is None or not isinstance(parent, dict):
            return None

    result = parent.get(parts.pop())
    if _is_xml_null(result):
        return None
    return result


class ResponseData:
    def __init__(self, json_data: dict):
        self.data = json_data

    def _get_value(self, key: str):
        """Nested values may be accessed by inserting a dot between nested keys.

        e.g. _get_value('top.middle.bottom') -> top.get('middle').get('bottom')"""
        if "." in key:
            return _get_nested_value(self.data, key)

        result = self.data.get(key)
        if _is_xml_null(result):
            return None
        if isinstance(result, str):
            result = result.strip()
        return result

    def _get_list(self, key: str) -> List:
        return coerce_to_list(self._get_value(key))

    def _get_str(self, key: str) -> Optional[str]:
        return coerce_to_str(self._get_value(key))

    def _get_int(self, key: str) -> Optional[int]:
        return coerce_to_int(self._get_value(key))

    def _get_boolean(self, key: str) -> Optional[bool]:
        return coerce_to_boolean(self._get_value(key))

    def _get_date(self, key: str) -> Optional[datetime.date]:
        return coerce_to_date(self._get_value(key))

    def _get_response_list(self, key, response_class: Type):
        objects = self._get_list(key)
        return [response_class(o) for o in objects]

    def __str__(self):
        return f"{self.data}"


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
        return self._get_str(f"{member_contract.PARTY}.{member_contract.PARTY_NAME}")

    def get_party_id(self) -> Optional[int]:
        return self._get_int(f"{member_contract.PARTY}.{member_contract.PARTY_ID}")

    def get_is_active(self) -> bool:
        return self._get_boolean(
            f"{status_contract.CURRENT_STATUS}.{status_contract.IS_ACTIVE}"
        )


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
    def get_constituency_id(self) -> Optional[int]:
        return self._get_int(constituencies_contract.PARLIAMENTDOTUK)

    def get_constituency_name(self) -> Optional[str]:
        return self._get_str(constituencies_contract.NAME)

    def get_start_date(self) -> datetime.date:
        return self._get_date(constituencies_contract.START_DATE)

    def get_end_date(self) -> datetime.date:
        return self._get_date(constituencies_contract.END_DATE)

    def get_election(self) -> Optional["ElectionResponseData"]:
        return ElectionResponseData(self._get_value(election_contract.ELECTION))


class ElectionResponseData(ResponseData):
    def get_election_id(self) -> Optional[int]:
        return self._get_int(election_contract.PARLIAMENTDOTUK)

    def get_election_name(self) -> str:
        return self._get_str(election_contract.NAME)

    def get_election_date(self) -> datetime.date:
        return self._get_date(election_contract.DATE)

    def get_election_type(self) -> Optional[str]:
        return self._get_str(election_contract.TYPE)


class PartyResponseData(ResponseData):
    def get_party_id(self) -> Optional[int]:
        return self._get_int(party_contract.PARLIAMENTDOTUK)

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

    def get_chair(self) -> List["CommitteeChairResponseData"]:
        return self._get_response_list(
            committee_contract.CHAIR_GROUP_KEY, CommitteeChairResponseData
        )


class CommitteeChairResponseData(ResponseData):
    def get_start_date(self) -> Optional[datetime.date]:
        return self._get_date(committee_contract.START_DATE)

    def get_end_date(self) -> Optional[datetime.date]:
        return self._get_date(committee_contract.END_DATE)


class PostResponseData(ResponseData):
    def get_post_id(self) -> Optional[int]:
        return self._get_int(posts_contract.PARLIAMENTDOTUK)

    def get_post_name(self) -> Optional[str]:
        return self._get_str(posts_contract.NAME)

    def get_post_hansard_name(self) -> Optional[str]:
        return self._get_str(posts_contract.HANSARD_NAME)

    def get_start_date(self) -> Optional[datetime.date]:
        return self._get_date(posts_contract.START_DATE)

    def get_end_date(self) -> Optional[datetime.date]:
        return self._get_date(posts_contract.END_DATE)

    def __str__(self):
        return f"{self.data}"


class AddressResponseData(ResponseData):
    def get_type(self) -> Optional[str]:
        return self._get_str(address_contract.TYPE)

    def get_is_physical(self) -> Optional[bool]:
        return self._get_boolean(address_contract.IS_PHYSICAL)

    def get_address(self) -> Optional[str]:
        address_lines = [self._get_str(key) for key in address_contract.ADDRESS_LINES]
        address = ", ".join([x for x in address_lines if x])
        return address

    def get_postcode(self) -> Optional[str]:
        return self._get_str(address_contract.POSTCODE)

    def get_phone(self) -> Optional[str]:
        return self._get_str(address_contract.PHONE)

    def get_fax(self) -> Optional[str]:
        return self._get_str(address_contract.FAX)

    def get_email(self) -> Optional[str]:
        return self._get_str(address_contract.EMAIL)


class InterestResponseData(ResponseData):
    def get_interest_id(self) -> Optional[int]:
        return self._get_int(interests_contract.PARLIAMENTDOTUK)

    def get_title(self) -> Optional[str]:
        return self._get_str(interests_contract.INTEREST_TITLE)

    def get_registered_late(self) -> Optional[bool]:
        return self._get_boolean(interests_contract.INTEREST_REGISTERD_LATE)

    def get_date_created(self) -> Optional[datetime.date]:
        return self._get_date(interests_contract.INTEREST_CREATED)

    def get_date_amended(self) -> Optional[datetime.date]:
        return self._get_date(interests_contract.INTEREST_AMENDED)

    def get_date_deleted(self) -> Optional[datetime.date]:
        return self._get_date(interests_contract.INTEREST_DELETED)


class DeclaredInterestCategoryResponseData(ResponseData):
    def get_category_id(self) -> Optional[int]:
        return self._get_int(interests_contract.PARLIAMENTDOTUK)

    def get_category_name(self) -> Optional[str]:
        return self._get_str(interests_contract.CATEGORY_NAME)

    def get_interests(self) -> List[InterestResponseData]:
        return [
            InterestResponseData(interest)
            for interest in coerce_to_list(
                self._get_value(interests_contract.INTEREST_GROUP_KEY)
            )
        ]


class ExperiencesResponseData(ResponseData):
    def get_type(self) -> Optional[str]:
        return self._get_str(experience_contract.TYPE)

    def get_organisation(self) -> Optional[str]:
        return self._get_str(experience_contract.ORGANISATION)

    def get_title(self) -> Optional[str]:
        return self._get_str(experience_contract.TITLE)

    def get_start_date(self) -> Optional[datetime.date]:
        return self._get_date(experience_contract.START_DATE)

    def get_end_date(self) -> Optional[datetime.date]:
        return self._get_date(experience_contract.END_DATE)


class SubjectsOfInterestResponseData(ResponseData):
    def get_category(self) -> Optional[str]:
        return self._get_str(bio_entries_contract.CATEGORY)

    def get_entry(self) -> Optional[str]:
        return self._get_str(bio_entries_contract.ENTRY)


class ContestedElectionResponseData(ResponseData):
    def get_election(self) -> Optional[ElectionResponseData]:
        return ElectionResponseData(self._get_value(contested_contract.ELECTION))

    def get_constituency_name(self) -> Optional[str]:
        return self._get_str(contested_contract.CONSTITUENCY)


class MemberBiographyResponseData(MemberResponseData):
    def get_basic_info(self) -> "BasicInfoResponseData":
        return BasicInfoResponseData(self._get_value(basic_contract.BASIC_DETAILS))

    def get_house_memberships(self) -> List["HouseMembershipResponseData"]:
        return self._get_response_list(
            houses_contract.GROUP_KEY, HouseMembershipResponseData
        )

    def get_constituencies(self) -> List["ConstituencyResponseData"]:
        return self._get_response_list(
            constituencies_contract.GROUP_KEY, ConstituencyResponseData
        )

    def get_parties(self) -> List["PartyResponseData"]:
        return self._get_response_list(party_contract.GROUP_KEY, PartyResponseData)

    def get_committees(self) -> List["CommitteeResponseData"]:
        return self._get_response_list(
            committee_contract.GROUP_KEY, CommitteeResponseData
        )

    def get_maiden_speeches(self) -> List["SpeechResponseData"]:
        return self._get_response_list(speech_contract.GROUP_KEY, SpeechResponseData)

    def get_goverment_posts(self) -> List["PostResponseData"]:
        return self._get_response_list(
            posts_contract.GOVERNMENT_GROUP_KEY, PostResponseData
        )

    def get_parliament_posts(self) -> List["PostResponseData"]:
        return self._get_response_list(
            posts_contract.PARLIAMENTARY_GROUP_KEY, PostResponseData
        )

    def get_opposition_posts(self) -> List["PostResponseData"]:
        return self._get_response_list(
            posts_contract.OPPOSITION_GROUP_KEY, PostResponseData
        )

    def get_addresses(self) -> List["AddressResponseData"]:
        return self._get_response_list(address_contract.GROUP_KEY, AddressResponseData)

    def get_subjects_of_interest(self) -> List["SubjectsOfInterestResponseData"]:
        return self._get_response_list(
            bio_entries_contract.GROUP_KEY, SubjectsOfInterestResponseData
        )

    def get_declared_interest_categories(
        self,
    ) -> List["DeclaredInterestCategoryResponseData"]:
        return self._get_response_list(
            interests_contract.CATEGORY_GROUP_KEY, DeclaredInterestCategoryResponseData
        )

    def get_experiences(self) -> List["ExperiencesResponseData"]:
        return self._get_response_list(
            experience_contract.GROUP_KEY, ExperiencesResponseData
        )

    def get_contested_elections(self) -> List["ContestedElectionResponseData"]:
        return self._get_response_list(
            contested_contract.GROUP_KEY, ContestedElectionResponseData
        )


def update_members(
    endpoint_url: str,
    update_member_func: Callable[[ResponseData], Optional[str]],
    response_class: Type[ResponseData],
    notification: TaskNotification,
    cache: Optional[JsonResponseCache] = None,
) -> None:
    response = get_json(endpoint_url, using_cache=cache)
    try:
        members = response.get("Members").get("Member")

        if not isinstance(members, list):
            members = [members]

    except AttributeError as e:
        notification.append(f"Failed to read item list for url={endpoint_url}")
        notification.mark_as_failed(e)
        return

    for member in members:
        try:
            update_member_func(response_class(member))
        except Exception as e:
            message = f"Failed to update member=[{member.__str__()[:64]}...]: {e}"
            notification.append(message)
            notification.mark_as_failed(e)
            return
