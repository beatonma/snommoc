from datetime import date
from typing import List

from api.schema.address import AddressSchema
from api.schema.party import PartyMiniSchema
from django.template.context_processors import static
from ninja import Schema
from ninja.schema import Resolver

from .constituency import ConstituencyMiniSchema, HistoricalConstituencySchema
from .types import FullSchema, MiniSchema, Name, ParliamentId, ParliamentSchema, alias


class TownSchema(Schema):
    town: Name
    country: Name


class ExperienceSchema(Schema):
    category: str | None = alias("category.name")
    organisation: str | None
    title: str | None
    start: date | None
    end: date | None


class CommitteeChairSchema(Schema):
    start: date | None
    end: date | None


class CommitteeMemberSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = alias("committee.parliamentdotuk")
    name: Name = alias("committee.name")
    chair: List[CommitteeChairSchema] = alias("committeechair_set")


class HouseMembershipSchema(Schema):
    house: Name = alias("house.name")
    start: date | None
    end: date | None


class DeclaredInterestsSchema(ParliamentSchema):
    category: str | None = alias("category.name")
    description: str | None
    created: date | None
    amended: date | None
    deleted: date | None
    registered_late: bool


class MaidenSpeechSchema(Schema):
    house: str = alias("house.name")
    date: date
    subject: str | None
    hansard: str | None


class PartyAffiliationSchema(Schema):
    party: PartyMiniSchema
    start: date | None
    end: date | None


class SubjectOfInterestSchema(Schema):
    category: str = alias("category.title")
    subject: str


class PostSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = alias("post.parliamentdotuk")
    name: Name = alias("post.name")
    hansard: str | None = alias("post.hansard_name")
    start: date | None
    end: date | None


class PostsSchema(Schema):
    governmental: List[PostSchema] = alias("governmentpostmember_set")
    parliamentary: List[PostSchema] = alias("parliamentarypostmember_set")
    opposition: List[PostSchema] = alias("oppositionpostmember_set")


class MemberMiniSchema(MiniSchema, ParliamentSchema):
    name: Name
    current_post: str | None
    party: PartyMiniSchema | None
    constituency: ConstituencyMiniSchema | None
    portrait: str | None = alias("memberportrait.square_url")


class MemberProfileSchema(ParliamentSchema):
    name: Name
    current_post: str | None
    party: PartyMiniSchema | None
    constituency: ConstituencyMiniSchema | None
    portrait: str | None = alias("memberportrait.wide_url")
    full_title: str | None
    given_name: Name | None
    family_name: Name | None
    active: bool
    is_mp: bool
    is_lord: bool
    date_of_birth: date | None
    date_of_death: date | None
    age: int
    gender: str | None
    place_of_birth: TownSchema | None = alias("town_of_birth")


def _resolve_self(obj):
    return obj


class MemberFullSchema(FullSchema):
    canary: str
    profile: MemberProfileSchema
    address: AddressSchema

    parties: List[PartyAffiliationSchema]
    constituencies: List[HistoricalConstituencySchema] = alias("constituencyresult_set")
    posts: PostsSchema
    committees: List[CommitteeMemberSchema] = alias("committeemember_set")
    experiences: List[ExperienceSchema] = alias("experience_set")
    houses: List[HouseMembershipSchema] = alias("housemembership_set")
    interests: List[DeclaredInterestsSchema] = alias("declaredinterest_set")
    speeches: List[MaidenSpeechSchema] = alias("maidenspeech_set")
    subjects: List[SubjectOfInterestSchema] = alias("subjectofinterest_set")

    @staticmethod
    def resolve_canary(obj):
        return "API V2 HELLO"

    @staticmethod
    def resolve_profile(obj):
        return obj

    @staticmethod
    def resolve_address(obj):
        return obj

    @staticmethod
    def resolve_posts(obj):
        return obj
