from datetime import date
from typing import Self

from crawlers.parliamentdotuk.tasks.openapi.parties.schema import Party
from crawlers.parliamentdotuk.tasks.types import (
    CoercedDate,
    CoercedDateTime,
    CoercedList,
    CoercedPhoneNumber,
    CoercedStr,
    PersonName,
    field,
)
from pydantic import BaseModel as Schema
from pydantic import Field, model_validator
from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS


class MemberStatus(Schema):
    status_id: int = field("statusId")
    is_active: bool = field("statusIsActive")
    description: str | None = field("statusDescription", default=None)
    notes: str | None = field("statusNotes", default=None)
    status_start: CoercedDate = field("statusStartDate")


class LatestHouseMembership(Schema):
    membershipFrom: CoercedStr
    house: int
    membershipStartDate: CoercedDate
    membershipEndDate: CoercedDate


class MemberBasic(Schema):
    parliamentdotuk: int = field("id")
    name: PersonName = field("nameDisplayAs")
    full_title: CoercedStr = field("nameFullTitle")
    gender: CoercedStr
    party: Party | None = field("latestParty")
    status: MemberStatus | None = field(
        "latestHouseMembership.membershipStatus", default=None
    )
    house: CoercedStr = Field(default=None)
    lords_type: CoercedStr = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def validate(cls, obj):
        house_membership = obj.get("latestHouseMembership")
        if house_membership:
            house_membership = LatestHouseMembership.model_validate(house_membership)
            if house_membership.house == 1:
                obj["house"] = HOUSE_OF_COMMONS
            if house_membership.house == 2:
                obj["lords_type"] = house_membership.membershipFrom
                obj["house"] = HOUSE_OF_LORDS

        return obj


class ConstituencyRepresentation(Schema):
    constituency_id: int = field("id")
    constituency_name: CoercedStr = field("name")
    constituency_start: CoercedDate = field(
        "constituencyStart",
        description="Start of the constituency's existence",
    )
    constituency_end: CoercedDate = field(
        "constituencyEnd",
        description="End of the constituency's existence",
    )
    representation_start: CoercedDate = field(
        "startDate",
        description="When this person became the constituency representative",
    )
    representation_end: CoercedDate = field(
        "endDate",
        description="When this person stopped being the constituency representative",
    )


class ContestedElection(Schema):
    constituency_id: int = field("id")
    constituency_name: CoercedStr = field("name")
    date: CoercedDate = field("startDate")


class HouseMembership(Schema):
    house_id: int = field("id")
    house_name: CoercedStr = field("name")
    start: CoercedDate = field("startDate")
    end: CoercedDate = field("endDate")


class Post(Schema):
    parliamentdotuk: int = field("id")
    name: CoercedStr
    start: CoercedDate = field("startDate")
    end: CoercedDate = field("endDate")
    additional_info: CoercedStr = field("additionalInfo")
    additional_info_link: CoercedStr = field("additionalInfoLink")


class PartyAffiliation(Schema):
    party_id: int = field("id")
    party_name: CoercedStr = field("name")
    start: CoercedDate = field("startDate")
    end: CoercedDate = field("endDate")


class CommitteeMembership(Schema):
    committee_id: int = field("id")
    committee_name: CoercedStr = field("name")
    start: CoercedDate = field("startDate")
    end: CoercedDate = field("endDate")


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
    type_name: CoercedStr = field("type")
    type_description: CoercedStr = field("typeDescription", default=None)
    is_preferred: bool = field("isPreferred")
    is_web_address: bool = field("isWebAddress")
    notes: CoercedStr = field("notes", default=None)
    address: CoercedStr  # See validate_address method
    postcode: CoercedStr = field("postcode", default=None)
    phone: CoercedPhoneNumber = field("phone", default=None)
    fax: CoercedPhoneNumber = field("fax", default=None)
    email: CoercedStr = field("email", default=None)

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
    type: CoercedStr = field("type")
    type_id: int = field("typeId")
    title: CoercedStr
    organisation: CoercedStr
    start: CoercedDate = Field(default=None)  # see validate_dates method
    end: CoercedDate = Field(default=None)  # see validate_dates method

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
    interest_title: CoercedStr = field("interest")
    created_at: CoercedDateTime = field("createdWhen")
    last_amended_at: CoercedDateTime = field("lastAmendedWhen")
    deleted_at: CoercedDateTime = field("deletedWhen")
    is_correction: bool = field("isCorrection")
    child_interests: CoercedList[Self] = field("childInterests")


class RegisteredInterestCategory(Schema):
    category_id: int = field("id")
    name: CoercedStr
    interests: CoercedList[RegisteredInterest]


class SubjectOfInterest(Schema):
    category: CoercedStr
    descriptions: CoercedList[CoercedStr] = field("focus")
