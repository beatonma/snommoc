from api.schema.includes import MinimalMemberSchema, PartyMiniSchema
from api.schema.types import Name, ParliamentSchema, field


class ConstituencyMapMP(MinimalMemberSchema):
    party: PartyMiniSchema | None


class ConstituencyMapSchema(ParliamentSchema):
    name: Name
    mp: ConstituencyMapMP | None
    boundary: str | None = field("boundary.simple_json", default=None)


class PartyMapSchema(PartyMiniSchema):
    territory: str | None = field("territory.geometry.json", default=None)
