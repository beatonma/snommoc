from datetime import date

from ninja import Schema

from .election import ElectionSchema
from .includes import MemberMiniSchema, PartyMiniSchema
from .types import AdministrativeName, ParliamentSchema, PersonName, field

__all__ = ["ConstituencyFullSchema"]


class ConstituencyCandidateSchema(Schema):
    name: PersonName
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
    name: AdministrativeName
    start: date | None
    end: date | None
    mp: MemberMiniSchema | None
    boundary: str | None = field("boundary.geometry.json", default=None)
    results: list[ResultsSchema]
