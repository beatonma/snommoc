from datetime import date

from ninja import Schema

from .election import ElectionSchema
from .includes import MemberMiniSchema, MinimalMemberSchema, PartyMiniSchema
from .types import Name, ParliamentSchema, field

__all__ = ["ConstituencyFullSchema", "NationalMapSchema"]


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
    boundary: str | None = field("boundary.geometry.json", default=None)
    results: list[ResultsSchema]


class NationalMapMP(MinimalMemberSchema):
    party: PartyMiniSchema | None


class NationalMapSchema(ParliamentSchema):
    name: Name
    mp: NationalMapMP | None
    boundary: str | None = field("boundary.simple_json", default=None)
