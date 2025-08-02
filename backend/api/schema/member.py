from datetime import date
from typing import Self

from ninja import Schema

from repository.models.houses import HouseType

from .includes import (
    BaseDivisionVote,
    ConstituencyMiniSchema,
    DivisionMiniSchema,
    MemberMiniSchema,
    OrganisationSchema,
    PartyMiniSchema,
)
from .types import (
    AdministrativeName,
    EmailAddress,
    ParliamentId,
    ParliamentSchema,
    PersonName,
    PhoneNumber,
    Url,
    WikipediaPath,
    field,
)

__all__ = [
    "MemberCareerHistory",
    "MemberProfile",
    "DivisionWithVoteSchema",
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
    description: str | None = field("type.description")


class AddressSchema(Schema):
    physical: list[PhysicalAddressSchema] = field("physical_addresses")
    web: list[WebAddressSchema] = field("web_addresses")


class TownSchema(Schema):
    town: AdministrativeName
    country: AdministrativeName


class ConstituencyRepresentation(Schema):
    constituency: ConstituencyMiniSchema
    start: date
    end: date | None


class ExperienceSchema(Schema):
    category: str | None = field("category.name")
    organisation: OrganisationSchema | None
    title: str | None
    start: date | None
    end: date | None


class CommitteeMemberSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = field("committee.parliamentdotuk")
    name: AdministrativeName = field("committee.name")
    start: date | None
    end: date | None


class HouseMembershipSchema(Schema):
    house: HouseType = field("house.name")
    start: date | None
    end: date | None


class RegisteredInterestDescriptionData(Schema):
    table: list[tuple[str, str | int]]
    additional_values: list[str]
    registration_dates: list[tuple[str, str]]
    start: str | None
    end: str | None


class RegisteredInterestSchema(ParliamentSchema):
    category: str | None = field("category.name")
    description: RegisteredInterestDescriptionData
    created: date | None
    amended: date | None
    deleted: date | None
    children: list[Self] = field("children")

    @staticmethod
    def resolve_description(obj):
        if not obj.description_data:
            raise ValueError(f"RegisteredInterests.description_data is not set: {obj}")

        return RegisteredInterestDescriptionData.model_validate(obj.description_data)


class PartyAffiliationSchema(Schema):
    party: PartyMiniSchema
    start: date | None
    end: date | None


class PostSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = field("post.parliamentdotuk")
    type: str = field("post.type")
    name: AdministrativeName = field("post.name")
    hansard: str | None = field("post.hansard_name")
    start: date | None
    end: date | None


class PortraitSchema(Schema):
    full: str | None = field("fullsize_url", default=None)
    square: str | None = field("square_url", default=None)
    wide: str | None = field("wide_url", default=None)
    tall: str | None = field("tall_url", default=None)


class MemberStatus(Schema):
    is_current: bool
    is_active: bool
    description: str | None
    extra_notes: str | None = field("notes")
    since: date | None = field("start")


class MemberProfile(MemberMiniSchema, ParliamentSchema):
    name: PersonName
    current_posts: list[str]
    party: PartyMiniSchema | None
    constituency: ConstituencyMiniSchema | None
    portrait: PortraitSchema | None = field("memberportrait", default=None)
    full_title: str | None
    status: MemberStatus
    house: HouseType | None = field("house.name", default=None)
    date_of_birth: date | None
    date_of_death: date | None
    age: int
    gender: str | None
    place_of_birth: TownSchema | None = field("town_of_birth")
    current_committees: list[CommitteeMemberSchema]
    address: AddressSchema
    wikipedia: WikipediaPath | None

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
    subjects_of_interest: dict[str, list[str]]
    interests: list[RegisteredInterestSchema]

    @staticmethod
    def resolve_subjects_of_interest(obj) -> dict[str, list]:
        qs = obj.subjects_of_interest.order_by("category__title")
        grouped = {}

        for item in qs:
            current = grouped.get(item.category.title, [])
            grouped[item.category.title] = current + [item.description]

        return grouped

    @staticmethod
    def resolve_interests(obj) -> list[RegisteredInterestSchema]:
        qs = obj.registered_interests.filter(parent__isnull=True)
        return qs


class DivisionWithVoteSchema(BaseDivisionVote):
    division: DivisionMiniSchema
