from datetime import date

from ninja import Schema

from .election import ElectionSchema
from .mini import ConstituencyMiniSchema, MemberMiniSchema, PartyMiniSchema
from .types import FullSchema, Name, ParliamentSchema, field

__all__ = [
    "ConstituencyFullSchema",
]


class ResultsSchema(Schema):
    election: ElectionSchema
    mp: MemberMiniSchema


class BoundarySchema(Schema):
    kml: str = field("boundary_kml")
    center_latitude: str
    center_longitude: str
    area: str
    boundary_length: str


class ConstituencyFullSchema(FullSchema, ParliamentSchema):
    name: Name
    start: date | None
    end: date | None
    mp: MemberMiniSchema | None
    boundary: BoundarySchema | None = field("constituencyboundary", default=None)
    results: list[ResultsSchema] = field("constituencyresult_set")


class ConstituencyCandidateSchema(Schema):
    name: Name
    profile: MemberMiniSchema | None = field("person")
    party_name: Name
    party: PartyMiniSchema | None
    order: int
    votes: int


class ConstituencyResultSchema(ParliamentSchema):
    electorate: int
    turnout: int
    turnout_fraction: float
    result: str
    majority: int
    constituency: ConstituencyMiniSchema = field("constituency_result.constituency")
    election: ElectionSchema = field("constituency_result.election")
    candidates: list[ConstituencyCandidateSchema]
