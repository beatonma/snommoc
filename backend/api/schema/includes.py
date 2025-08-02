from datetime import date, datetime

from ninja import Schema

from api.schema.types import (
    AdministrativeName,
    DivisionVoteType,
    House,
    ParliamentSchema,
    PersonName,
    Safe,
    Title,
    Url,
    field,
)
from repository.models import Constituency

__all__ = [
    "ConstituencyMiniSchema",
    "BillMiniSchema",
    "DivisionMiniSchema",
    "MemberMiniSchema",
    "MinimalMemberSchema",
    "OrganisationSchema",
    "BasePartySchema",
    "PartyMiniSchema",
    "ItemThemeSchema",
    "BaseDivisionVote",
]


class ItemThemeSchema(Schema):
    primary: str = field("primary")
    on_primary: str = field("on_primary")
    accent: str = field("accent")
    on_accent: str = field("on_accent")


class BasePartySchema(ParliamentSchema):
    theme: ItemThemeSchema | None

    @staticmethod
    def resolve_theme(obj):
        try:
            return obj.theme
        except AttributeError:
            # One-to-one rel Does not exist
            pass


class PartyMiniSchema(BasePartySchema):
    name: AdministrativeName
    logo: str | None
    logo_mask: str | None
    active_mp_count: int | None = None
    active_lord_count: int | None = None

    @staticmethod
    def resolve_name(obj):
        return obj.short_name or obj.name


class _ConstituencyMemberSchema(ParliamentSchema):
    """Simple member data for embedding in constituency"""

    name: PersonName
    party: PartyMiniSchema | None


class ConstituencyMiniSchema(ParliamentSchema):
    name: AdministrativeName
    start: date | None
    end: date | None
    mp: _ConstituencyMemberSchema | None


class _MemberConstituencySchema(ParliamentSchema):
    """Simple constituency data for embedding in member"""

    name: AdministrativeName
    start: date | None
    end: date | None


class MemberPortrait(Schema):
    fullsize_url: Url | None
    square_url: Url | None
    tall_url: Url | None
    wide_url: Url | None


class MinimalMemberSchema(ParliamentSchema):
    name: PersonName
    portrait: MemberPortrait | None = field("memberportrait", default=None)


class MemberMiniSchema(MinimalMemberSchema):
    name: PersonName
    current_posts: list[str]
    party: PartyMiniSchema | None
    constituency: _MemberConstituencySchema | None
    lord_type: str | None = field("lords_type.name", default=None)

    @staticmethod
    def resolve_constituency(obj):
        try:
            return obj.constituency
        except Constituency.DoesNotExist:
            pass

    @staticmethod
    def resolve_current_posts(obj):
        return obj.current_posts()


class DivisionMiniSchema(ParliamentSchema):
    title: Title
    house: House
    date: date
    is_passed: bool


class BaseDivisionVote(Schema):
    vote: DivisionVoteType

    @staticmethod
    def resolve_vote(obj) -> DivisionVoteType:
        vote_type = obj.vote_type.name
        if vote_type == "aye" or vote_type == "content":
            return "aye"
        if vote_type == "no" or vote_type == "not_content":
            return "no"
        return vote_type


class BillMiniSchema(ParliamentSchema):
    title: Title
    description: str | None = field("summary", default=None)
    last_update: datetime
    current_house: Safe[House]


class OrganisationSchema(Schema):
    name: AdministrativeName
    slug: str
    url: Url | None
