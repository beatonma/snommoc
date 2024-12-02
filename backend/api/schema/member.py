from datetime import date

from ninja import Schema

from .includes import (
    ConstituencyMiniSchema,
    DivisionMiniSchema,
    MemberMiniSchema,
    PartyMiniSchema,
)
from .types import (
    EmailAddress,
    Name,
    ParliamentId,
    ParliamentSchema,
    PhoneNumber,
    Url,
    field,
)

__all__ = [
    "MemberCareerHistory",
    "MemberProfile",
    "MemberVotesSchema",
]


class PhysicalAddressSchema(Schema):
    description: str | None = None
    address: str | None = None
    postcode: str | None = None
    phone: PhoneNumber | None
    fax: PhoneNumber | None
    email: EmailAddress | None = None


class WebAddressSchema(Schema):
    url: Url
    description: str | None


class AddressSchema(Schema):
    physical: list[PhysicalAddressSchema] = field("physical_addresses")
    web: list[WebAddressSchema] = field("web_addresses")


class TownSchema(Schema):
    town: Name
    country: Name


class ConstituencyRepresentation(Schema):
    constituency: ConstituencyMiniSchema
    start: date
    end: date | None


class ExperienceSchema(Schema):
    category: str | None = field("category.name")
    organisation: str | None
    title: str | None
    start: date | None
    end: date | None


class CommitteeMemberSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = field("committee.parliamentdotuk")
    name: Name = field("committee.name")
    start: date | None
    end: date | None


class HouseMembershipSchema(Schema):
    house: Name = field("house.name")
    start: date | None
    end: date | None


class DeclaredInterestsSchema(ParliamentSchema):
    category: str | None = field("category.name")
    description: str | None
    created: date | None
    amended: date | None
    deleted: date | None
    registered_late: bool


class PartyAffiliationSchema(Schema):
    party: PartyMiniSchema
    start: date | None
    end: date | None


class SubjectOfInterestSchema(Schema):
    category: str = field("category.title")
    description: str


class PostSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = field("post.parliamentdotuk")
    type: str = field("post.type")
    name: Name = field("post.name")
    hansard: str | None = field("post.hansard_name")
    start: date | None
    end: date | None


class PortraitSchema(Schema):
    full: str | None = field("fullsize_url", default=None)
    square: str | None = field("square_url", default=None)
    wide: str | None = field("wide_url", default=None)
    tall: str | None = field("tall_url", default=None)


class MemberStatus(Schema):
    is_active: bool
    description: str | None
    extra_notes: str | None = field("notes")


class MemberProfile(MemberMiniSchema, ParliamentSchema):
    name: Name
    current_posts: list[str]
    party: PartyMiniSchema | None
    constituency: ConstituencyMiniSchema | None
    portrait: PortraitSchema | None = field("memberportrait", default=None)
    full_title: str | None
    given_name: Name | None
    family_name: Name | None
    status: MemberStatus
    house: str | None = field("house.name", default=None)
    date_of_birth: date | None
    date_of_death: date | None
    age: int
    gender: str | None
    place_of_birth: TownSchema | None = field("town_of_birth")
    current_committees: list[CommitteeMemberSchema]
    address: AddressSchema
    subjects_of_interest: list[SubjectOfInterestSchema] = field("subjects_of_interest")

    @staticmethod
    def resolve_current_committees(obj):
        return obj.committees.filter(end=None).order_by("-start")

    @staticmethod
    def resolve_address(obj):
        return obj


class MemberCareerHistory(Schema):
    posts: list[PostSchema]
    parties: list[PartyAffiliationSchema] = field("party_affiliations")
    constituencies: list[ConstituencyRepresentation] = field("constituencies")
    committees: list[CommitteeMemberSchema] = field("committees")
    experiences: list[ExperienceSchema] = field("experiences")
    houses: list[HouseMembershipSchema] = field("house_memberships")
    interests: list[DeclaredInterestsSchema] = field("registered_interests")


class VoteSchema(Schema):
    division: DivisionMiniSchema
    vote: str = field("vote_type.name")


class MemberVotesSchema(Schema):
    commons: list[VoteSchema]
    lords: list[VoteSchema]
