from crawlers.parliamentdotuk.tasks.lda.schema import types
from crawlers.parliamentdotuk.tasks.types import field
from pydantic import BaseModel as Schema


class ElectionCandidate(Schema):
    name: types.NestedStr = field("fullName")
    number_of_votes: int = field("numberOfVotes")
    order: int
    party_name: types.NestedStr = field("party")


class ResultConstituency(Schema):
    parliamentdotuk: types.ParliamentId = field("_about")
    name: types.NestedStr = field("label")


class ResultElection(Schema):
    parliamentdotuk: types.ParliamentId = field("_about")
    name: types.NestedStr = field("label")


class ElectionResult(Schema):
    parliamentdotuk: types.ParliamentId = field("_about")
    constituency: ResultConstituency
    election: ResultElection
    electorate: int
    majority: int
    turnout: int
    result_of_election: str = field("resultOfElection")


class ElectionResultDetail(ElectionResult):
    candidates: list[ElectionCandidate] = field("candidate")
