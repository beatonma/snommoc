from datetime import date, datetime

from api.schema.party import PartyThemeSchema
from api.schema.types import MiniSchema, Name, ParliamentSchema, field
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
    theme: PartyThemeSchema | None

    @staticmethod
    def resolve_theme(obj):
        try:
            return obj.theme
        except AttributeError:
            # One-to-one rel Does not exist
            pass


class ConstituencyMiniSchema(MiniSchema, ParliamentSchema):
    name: Name


class MemberMiniSchema(MiniSchema, ParliamentSchema):
    name: Name
    current_post: str | None
    party: PartyMiniSchema | None
    constituency: ConstituencyMiniSchema | None
    portrait: str | None = field("memberportrait.square_url", default=None)


class DivisionMiniSchema(MiniSchema, ParliamentSchema):
    title: str
    date: date
    house: HouseType
    passed: bool


class BillMiniSchema(MiniSchema, ParliamentSchema):
    title: str
    description: str | None = field("summary", default=None)
    last_update: datetime
