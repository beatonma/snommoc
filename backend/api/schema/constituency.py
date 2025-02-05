from datetime import date

from ninja import Schema

from .election import ElectionSchema
from .includes import MemberMiniSchema, PartyMiniSchema
from .types import Name, ParliamentSchema, field

__all__ = ["ConstituencyFullSchema", "ConstituencyMapSchema"]


class ConstituencyCandidateSchema(Schema):
    name: Name
    profile: MemberMiniSchema | None = field("person", default=None)
    party: PartyMiniSchema | None
    order: int
    votes: int


class ResultsSchema(Schema):
    election: ElectionSchema
    winner: MemberMiniSchema | None
    electorate: int = field("detail.electorate")
    turnout: int = field("detail.turnout")
    result: str = field("detail.result")
    majority: int = field("detail.majority")
    candidates: list[ConstituencyCandidateSchema]

    @staticmethod
    def resolve_candidates(obj):
        return obj.detail.candidates.order_by("-votes")


class ConstituencyFullSchema(ParliamentSchema):
    name: Name
    start: date | None
    end: date | None
    mp: MemberMiniSchema | None
    boundary: dict | None = field("boundary.geo_json", default=None)
    results: list[ResultsSchema]


class ConstituencyMapSchema(ParliamentSchema):
    name: Name
    start: date | None
    end: date | None
    mp: MemberMiniSchema | None
    boundary: dict | None = field("simple_boundary.geo_json", default=None)
