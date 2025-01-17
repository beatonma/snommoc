import re
from datetime import date
from typing import Self

from crawlers.parliamentdotuk.tasks.openapi.parties.schema import Party
from crawlers.parliamentdotuk.tasks.types import (
    DateOrNone,
    DateTimeOrNone,
    House,
    List,
    PersonName,
    PhoneNumber,
    StringOrNone,
    StringOrNoneKeepBreaks,
    field,
)
from pydantic import BaseModel as Schema
from pydantic import Field, model_validator
from repository.models.houses import HOUSE_OF_LORDS


class _MemberStatus(Schema):
    """Used internally for MemberStatus validation."""

    status_id: int = field("statusId")
    is_active: bool = field("statusIsActive")
    description: str | None = field("statusDescription", default=None)
    notes: str | None = field("statusNotes", default=None)
    status_start: DateOrNone = field("statusStartDate")


class _LatestHouseMembership(Schema):
    """Used internally for MemberStatus validation."""

    membership_from: StringOrNone = field("membershipFrom")
    house: House
    membership_start_date: DateOrNone = field("membershipStartDate")
    membership_end_date: DateOrNone = field("membershipEndDate")
    membership_end_reason: StringOrNone = field("membershipEndReason")
    membership_end_reason_notes: StringOrNone = field("membershipEndReasonNotes")
    status: _MemberStatus | None = field("membershipStatus")


class MemberStatus(Schema):
    is_current: bool
    is_active: bool
    description: StringOrNone
    notes: StringOrNone
    since: DateOrNone

    house: House
    lords_type: StringOrNone

    @model_validator(mode="before")
    @classmethod
    def validate(cls, obj):
        """Use data from _LatestHouseMembership and its (optional) _MemberStatus
        to build an accurate current status for this member"""
        data = _LatestHouseMembership.model_validate(obj)
        status = data.status

        is_current = data.membership_end_date is None
        is_active = is_current
        status_description = data.membership_end_reason
        status_notes = data.membership_end_reason_notes
        status_since = data.membership_end_date or data.membership_start_date
        if status:
            is_active = is_active and status.is_active
            if not is_active:
                status_description = status.description or status_description
                status_notes = status.notes or status_notes
                status_since = status.status_start

        obj["is_current"] = is_current
        obj["is_active"] = is_active
        obj["description"] = status_description
        obj["notes"] = status_notes
        obj["since"] = status_since

        obj["house"] = data.house
        obj["lords_type"] = (
            data.membership_from if data.house == HOUSE_OF_LORDS else None
        )

        return obj


class MemberBasic(Schema):
    parliamentdotuk: int = field("id")
    name: PersonName = field("nameDisplayAs")
    list_as: StringOrNone = field("nameListAs")
    full_title: StringOrNone = field("nameFullTitle")
    gender: StringOrNone
    party: Party | None = field("latestParty")
    status: MemberStatus = field("latestHouseMembership")


class ConstituencyRepresentation(Schema):
    constituency_id: int = field("id")
    constituency_name: StringOrNone = field("name")
    constituency_start: DateOrNone = field(
        "constituencyStart",
        description="Start of the constituency's existence",
    )
    constituency_end: DateOrNone = field(
        "constituencyEnd",
        description="End of the constituency's existence",
    )
    representation_start: DateOrNone = field(
        "startDate",
        description="When this person became the constituency representative",
    )
    representation_end: DateOrNone = field(
        "endDate",
        description="When this person stopped being the constituency representative",
    )


class ContestedElection(Schema):
    constituency_id: int = field("id")
    constituency_name: StringOrNone = field("name")
    date: DateOrNone = field("startDate")


class HouseMembership(Schema):
    house_name: House = field("name")
    start: DateOrNone = field("startDate")
    end: DateOrNone = field("endDate")


class Post(Schema):
    parliamentdotuk: int = field("id")
    name: StringOrNone
    start: DateOrNone = field("startDate")
    end: DateOrNone = field("endDate")
    additional_info: StringOrNone = field("additionalInfo")
    additional_info_link: StringOrNone = field("additionalInfoLink")


class PartyAffiliation(Schema):
    party_id: int = field("id")
    party_name: StringOrNone = field("name")
    start: DateOrNone = field("startDate")
    end: DateOrNone = field("endDate")


class CommitteeMembership(Schema):
    committee_id: int = field("id")
    committee_name: StringOrNone = field("name")
    start: DateOrNone = field("startDate")
    end: DateOrNone = field("endDate")


class MemberBiography(Schema):
    representations: list[ConstituencyRepresentation]
    elections_contested: list[ContestedElection] = field("electionsContested")
    government_posts: list[Post] = field("governmentPosts")
    opposition_posts: list[Post] = field("oppositionPosts")
    other_posts: list[Post] = field("otherPosts")
    party_affiliations: list[PartyAffiliation] = field("partyAffiliations")
    committees: list[CommitteeMembership] = field("committeeMemberships")
    house_memberships: list[HouseMembership] = field("houseMemberships")


class ContactInfo(Schema):
    type_id: int = field("typeId")
    type_name: StringOrNone = field("type")
    type_description: StringOrNone = field("typeDescription", default=None)
    is_preferred: bool = field("isPreferred")
    is_web_address: bool = field("isWebAddress")
    notes: StringOrNone = field("notes", default=None)
    address: StringOrNone  # See validate_address method
    postcode: StringOrNone = field("postcode", default=None)
    phone: PhoneNumber = field("phone", default=None)
    fax: PhoneNumber = field("fax", default=None)
    email: StringOrNone = field("email", default=None)

    @model_validator(mode="before")
    @classmethod
    def validate_address(cls, obj):
        """Combine address fields into single string."""
        address_lines = [
            obj.get(key)
            for key in [
                "line1",
                "line2",
                "line3",
                "line4",
                "line5",
            ]
        ]
        address = ", ".join(x for x in address_lines if x)

        obj["address"] = address or None
        return obj


class Experience(Schema):
    experience_id: int = field("id")
    type: StringOrNone = field("type")
    type_id: int = field("typeId")
    title: StringOrNone
    organisation: StringOrNone
    start: DateOrNone = Field(default=None)  # see validate_dates method
    end: DateOrNone = Field(default=None)  # see validate_dates method

    @model_validator(mode="before")
    @classmethod
    def validate_dates(cls, obj):
        start_month = obj.get("startMonth")
        start_year = obj.get("startYear")
        end_month = obj.get("endMonth")
        end_year = obj.get("endYear")

        if start_year:
            obj["start"] = date(start_year, start_month or 1, 1)
        if end_year:
            obj["end"] = date(end_year, end_month or 12, 1)

        return obj


class RegisteredInterest(Schema):
    interest_id: int = field("id")
    interest_title: StringOrNoneKeepBreaks = field("interest")
    created_at: DateTimeOrNone = field("createdWhen")
    last_amended_at: DateTimeOrNone = field("lastAmendedWhen")
    deleted_at: DateTimeOrNone = field("deletedWhen")
    is_correction: bool = field("isCorrection")
    child_interests: List[Self] = field("childInterests")


class RegisteredInterestCategory(Schema):
    sort_order: int = field("sortOrder")
    name: StringOrNone
    codename_major: int
    codename_minor: StringOrNone
    interests: List[RegisteredInterest]

    @model_validator(mode="before")
    @classmethod
    def validate_codename(cls, obj):
        """Extract codename values from category name.

        Codename values are used for sorting categories correctly.
        e.g. "2. (b) Any other support not included in Category 2(a)" should
             yield codename_major=2, codename_minor="b"
        """
        name = obj["name"].removeprefix("Category ")

        match = re.match(
            r"^(?P<major>\d+)[:.] (\((?P<minor_start>[a-z]+)\) )?.*?( \((?P<minor_end>[a-z]+)\))?$",
            name,
        )
        groups = match.groupdict() if match else {}
        obj["codename_major"] = int(groups.get("major", 0))
        obj["codename_minor"] = groups.get("minor_start") or groups.get("minor_end")
        obj["name"] = name

        return obj


class SubjectOfInterest(Schema):
    category: StringOrNone
    descriptions: List[StringOrNone] = field("focus")
