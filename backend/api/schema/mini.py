from datetime import date, datetime

from api.schema.party import PartyThemeSchema
from api.schema.types import Name, ParliamentSchema, field
from repository.models import Constituency
from repository.models.houses import HouseType

__all__ = [
    "ConstituencyMiniSchema",
    "BillMiniSchema",
    "DivisionMiniSchema",
    "MemberMiniSchema",
    "PartyMiniSchema",
]


class PartyMiniSchema(ParliamentSchema):
    name: Name
    logo: str | None
    logo_mask: str | None
    theme: PartyThemeSchema | None

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
    passed: bool


class BillMiniSchema(ParliamentSchema):
    title: str
    description: str | None = field("summary", default=None)
    last_update: datetime
