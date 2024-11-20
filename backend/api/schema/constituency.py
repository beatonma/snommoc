from datetime import date

from ninja import Schema

from .election import ElectionSchema
from .mini import ConstituencyMiniSchema, MemberMiniSchema, PartyMiniSchema
from .types import FullSchema, Name, ParliamentSchema, field

__all__ = ["ConstituencyFullSchema", "ConstituencyResultSchema"]


class ResultsSchema(Schema):
    election: ElectionSchema
    mp: MemberMiniSchema | None


class ConstituencyFullSchema(FullSchema, ParliamentSchema):
    name: Name
    start: date | None
    end: date | None
    mp: MemberMiniSchema | None
    boundary: dict | None = field("constituencyboundary.geo_json", default=None)
    results: list[ResultsSchema] = field("constituencyresult_set")


class ConstituencyCandidateSchema(Schema):
    name: Name
    profile: MemberMiniSchema | None = field("person", default=None)
    party_name: Name
    party: PartyMiniSchema | None
    order: int
    votes: int


class ConstituencyResultSchema(Schema):
    electorate: int
    turnout: int
    result: str
    majority: int
    constituency: ConstituencyMiniSchema = field("constituency_result.constituency")
    election: ElectionSchema = field("constituency_result.election")
    candidates: list[ConstituencyCandidateSchema]
