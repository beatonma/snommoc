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
    primary: str
    on_primary: str
    accent: str
    on_accent: str


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


class ConstituencyMiniSchema(ParliamentSchema):
    name: Name
    start: date | None
    end: date | None


class MemberMiniSchema(ParliamentSchema):
    name: Name
    current_posts: list[str]
    party: PartyMiniSchema | None
    constituency: ConstituencyMiniSchema | None
    portrait: str | None = field("memberportrait.square_url", default=None)

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
