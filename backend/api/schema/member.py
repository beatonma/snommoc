from datetime import date

from ninja import Schema

from .election import ElectionSchema
from .mini import ConstituencyMiniSchema, DivisionMiniSchema, PartyMiniSchema
from .types import (
    EmailAddress,
    FullSchema,
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
    physical: list[PhysicalAddressSchema] = field("physicaladdress_set")
    web: list[WebAddressSchema] = field("webaddress_set")


class TownSchema(Schema):
    town: Name
    country: Name


class HistoricalConstituencySchema(Schema):
    constituency: ConstituencyMiniSchema
    election: ElectionSchema
    start: date
    end: date | None


class ExperienceSchema(Schema):
    category: str | None = field("category.name")
    organisation: str | None
    title: str | None
    start: date | None
    end: date | None


class CommitteeChairSchema(Schema):
    start: date | None
    end: date | None


class CommitteeMemberSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = field("committee.parliamentdotuk")
    name: Name = field("committee.name")
    chair: list[CommitteeChairSchema] = field("committeechair_set")
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


class MaidenSpeechSchema(Schema):
    house: str = field("house.name")
    date: date
    subject: str | None
    hansard: str | None


class PartyAffiliationSchema(Schema):
    party: PartyMiniSchema
    start: date | None
    end: date | None


class SubjectOfInterestSchema(Schema):
    category: str = field("category.title")
    subject: str


class PostSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = field("post.parliamentdotuk")
    name: Name = field("post.name")
    hansard: str | None = field("post.hansard_name")
    start: date | None
    end: date | None


class PostsSchema(Schema):
    governmental: list[PostSchema] = field("governmentpostmember_set")
    parliamentary: list[PostSchema] = field("parliamentarypostmember_set")
    opposition: list[PostSchema] = field("oppositionpostmember_set")


class MemberProfile(ParliamentSchema):
    name: Name
    current_post: str | None
    party: PartyMiniSchema | None
    constituency: ConstituencyMiniSchema | None
    portrait: str | None = field("memberportrait.wide_url", default=None)
    full_title: str | None
    given_name: Name | None
    family_name: Name | None
    active: bool
    house: str | None = field("house.name", default=None)
    date_of_birth: date | None
    date_of_death: date | None
    age: int
    gender: str | None
    place_of_birth: TownSchema | None = field("town_of_birth")
    current_committees: list[CommitteeMemberSchema]
    address: AddressSchema
    subjects_of_interest: list[SubjectOfInterestSchema] = field("subjectofinterest_set")

    @staticmethod
    def resolve_current_committees(obj):
        return obj.committeemember_set.filter(end=None).order_by("-start")

    @staticmethod
    def resolve_address(obj):
        return obj


class MemberCareerHistory(FullSchema):
    posts: PostsSchema
    parties: list[PartyAffiliationSchema]
    constituencies: list[HistoricalConstituencySchema] = field("constituencyresult_set")
    committees: list[CommitteeMemberSchema] = field("committeemember_set")
    experiences: list[ExperienceSchema] = field("experience_set")
    houses: list[HouseMembershipSchema] = field("housemembership_set")
    interests: list[DeclaredInterestsSchema] = field("declaredinterest_set")
    speeches: list[MaidenSpeechSchema] = field("maidenspeech_set")

    @staticmethod
    def resolve_posts(obj):
        return obj


class VoteSchema(Schema):
    division: DivisionMiniSchema
    vote: str = field("vote_type.name")


class MemberVotesSchema(Schema):
    commons: list[VoteSchema]
    lords: list[VoteSchema]
