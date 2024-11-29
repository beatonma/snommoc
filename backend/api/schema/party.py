from datetime import datetime

from api.schema.types import Name, ParliamentSchema, Url, WikipediaPath, field
from ninja import Schema

__all__ = ["PartyFullSchema", "PartyThemeSchema"]


class PartyThemeSchema(Schema):
    primary: str
    on_primary: str
    accent: str
    on_accent: str


class PartyDemographics(Schema):
    modified_at: datetime
    house: str = field("house.name")
    male_member_count: int
    female_member_count: int
    non_binary_member_count: int
    total_member_count: int


class PartyFullSchema(ParliamentSchema):
    name: Name
    short_name: Name | None
    long_name: Name | None
    homepage: Url | None
    year_founded: int | None
    wikipedia: WikipediaPath | None
    logo: str | None
    logo_mask: str | None
    demographics: list[PartyDemographics]
    theme: PartyThemeSchema | None

    @staticmethod
    def resolve_theme(obj):
        try:
            return obj.theme
        except AttributeError:
            # One-to-one rel Does not exist
            pass
