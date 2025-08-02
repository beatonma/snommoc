from pydantic import BaseModel as Schema

from crawlers.parliamentdotuk.tasks.openapi.parties.schema import Party
from crawlers.parliamentdotuk.tasks.types import field


class PartyGenderDemographics(Schema):
    party: Party
    male_member_count: int = field("male")
    female_member_count: int = field("female")
    non_binary_member_count: int = field("nonBinary")
    total_member_count: int = field("total")


class PartyLordsDemographics(Schema):
    party: Party
    life_count: int = field("life")
    hereditary_count: int = field("hereditary")
    bishop_count: int = field("bishop")
    total_count: int = field("total")
