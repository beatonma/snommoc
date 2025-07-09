from datetime import date, datetime

from api.schema.types import DivisionVoteType, Name, ParliamentSchema, field
from ninja import Schema
from pydantic import Field
from repository.models import Constituency
from repository.models.houses import HouseType

__all__ = [
    "ConstituencyMiniSchema",
    "BillMiniSchema",
    "DivisionMiniSchema",
    "MemberMiniSchema",
    "MinimalMemberSchema",
    "OrganisationSchema",
    "PartyMiniSchema",
    "ItemThemeSchema",
    "BaseDivisionVote",
    "IncludeHouse",
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
    name: Name
    logo: str | None
    logo_mask: str | None
    active_member_count: int
    active_commons_members: int | None = Field(default=None)

    @staticmethod
    def resolve_name(obj):
        return obj.short_name or obj.name


class _ConstituencyMemberSchema(ParliamentSchema):
    """Simple member data for embedding in constituency"""

    name: Name
    party: PartyMiniSchema | None


class ConstituencyMiniSchema(ParliamentSchema):
    name: Name
    start: date | None
    end: date | None
    mp: _ConstituencyMemberSchema | None


class _MemberConstituencySchema(ParliamentSchema):
    """Simple constituency data for embedding in member"""

    name: Name
    start: date | None
    end: date | None


class MinimalMemberSchema(ParliamentSchema):
    name: Name
    portrait: str | None = None
    # portrait: str | None = field("memberportrait.square_url", default=None)


class MemberMiniSchema(MinimalMemberSchema):
    name: Name
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


class IncludeHouse(Schema):
    house: HouseType

    @staticmethod
    def resolve_house(obj):
        return obj.house.name


class DivisionMiniSchema(IncludeHouse, ParliamentSchema):
    title: str
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
    title: str
    description: str | None = field("summary", default=None)
    last_update: datetime


class OrganisationSchema(Schema):
    name: str
    url: str | None
    slug: str
