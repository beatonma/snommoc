from crawlers.parliamentdotuk.tasks.lda.schema import types
from pydantic import BaseModel as Schema
from pydantic import Field


class ElectionCandidate(Schema):
    name: types.NestedStr = Field(validation_alias="fullName")
    number_of_votes: int = Field(validation_alias="numberOfVotes")
    order: int
    party_name: types.NestedStr = Field(validation_alias="party")


class ResultConstituency(Schema):
    parliamentdotuk: types.ParliamentId = Field(validation_alias="_about")
    name: types.NestedStr = Field(validation_alias="label")


class ResultElection(Schema):
    parliamentdotuk: types.ParliamentId = Field(validation_alias="_about")
    name: types.NestedStr = Field(validation_alias="label")


class ElectionResult(Schema):
    parliamentdotuk: types.ParliamentId = Field(validation_alias="_about")
    constituency: ResultConstituency
    election: ResultElection
    electorate: int
    majority: int
    turnout: int
    result_of_election: str = Field(validation_alias="resultOfElection")


class ElectionResultDetail(ElectionResult):
    candidates: list[ElectionCandidate] = Field(validation_alias="candidate")
