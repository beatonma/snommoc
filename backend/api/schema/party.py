from datetime import datetime

from ninja import Schema

from api.schema.includes import BasePartySchema
from api.schema.types import PersonName, Url, WikipediaPath, field

__all__ = ["PartyFullSchema"]


class GenderDemographics(Schema):
    modified_at: datetime
    house: str = field("house.name")
    male_member_count: int
    female_member_count: int
    non_binary_member_count: int
    total_member_count: int


class LordsDemographics(Schema):
    modified_at: datetime
    life_count: int
    hereditary_count: int
    bishop_count: int
    total_count: int


class PartyFullSchema(BasePartySchema):
    name: PersonName
    short_name: PersonName | None
    long_name: PersonName | None
    homepage: Url | None
    year_founded: int | None
    wikipedia: WikipediaPath | None
    logo: str | None
    logo_mask: str | None
    active_mp_count: int | None = None
    active_lord_count: int | None = None
    gender_demographics: list[GenderDemographics]
    lords_demographics: LordsDemographics | None = field(
        "lords_demographics", default=None
    )
