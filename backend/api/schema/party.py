from datetime import datetime

from api.schema.includes import BasePartySchema
from api.schema.types import Name, Url, WikipediaPath, field
from ninja import Schema

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
    name: Name
    short_name: Name | None
    long_name: Name | None
    homepage: Url | None
    year_founded: int | None
    wikipedia: WikipediaPath | None
    logo: str | None
    logo_mask: str | None
    active_member_count: int
    gender_demographics: list[GenderDemographics]
    lords_demographics: LordsDemographics | None = field(
        "lords_demographics", default=None
    )
