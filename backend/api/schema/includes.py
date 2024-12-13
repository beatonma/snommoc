from datetime import date, datetime

from api.schema.types import Name, ParliamentSchema, field
from ninja import Schema
from pydantic import Field
from repository.models import Constituency
from repository.models.houses import HouseType

__all__ = [
    "ConstituencyMiniSchema",
    "BillMiniSchema",
    "DivisionMiniSchema",
    "MemberMiniSchema",
    "PartyMiniSchema",
    "PartyThemeSchema",
]


class PartyThemeSchema(Schema):
    primary: str = field("rgb_primary")
    on_primary: str = field("rgb_on_primary")
    accent: str = field("rgb_accent")
    on_accent: str = field("rgb_on_accent")


class PartyMiniSchema(ParliamentSchema):
    name: Name
    logo: str | None
    logo_mask: str | None
    theme: PartyThemeSchema | None
    active_member_count: int
    active_commons_members: int | None = Field(default=None)

    @staticmethod
    def resolve_name(obj):
        return obj.short_name or obj.name

    @staticmethod
    def resolve_theme(obj):
        try:
            return obj.theme
        except AttributeError:
            # One-to-one rel Does not exist
            pass


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


class MemberMiniSchema(ParliamentSchema):
    name: Name
    current_posts: list[str]
    party: PartyMiniSchema | None
    constituency: ConstituencyMiniSchema | None
    portrait: str | None = field("memberportrait.square_url", default=None)
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
    title: str
    date: date
    house: HouseType
    is_passed: bool


class BillMiniSchema(ParliamentSchema):
    title: str
    description: str | None = field("summary", default=None)
    last_update: datetime
