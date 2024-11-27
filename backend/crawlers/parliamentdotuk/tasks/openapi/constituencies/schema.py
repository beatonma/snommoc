import json
from typing import Annotated

from crawlers.parliamentdotuk.tasks.openapi.members.schema import MemberBasic
from crawlers.parliamentdotuk.tasks.openapi.parties.schema import Party
from crawlers.parliamentdotuk.tasks.types import (
    CoercedDate,
    field,
    PersonName,
    CoercedStr,
)
from pydantic import BaseModel as Schema
from pydantic import BeforeValidator


class Constituency(Schema):
    parliamentdotuk: int = field("id")
    name: str
    start_date: CoercedDate = field("startDate")
    end_date: CoercedDate = field("endDate")
    member: MemberBasic | None = field("currentRepresentation.member.value")


class ConstituencyBoundary(Schema):
    geo_json: Annotated[dict, BeforeValidator(json.loads)] = field("value")


class ElectionCandidate(Schema):
    parliamentdotuk: int | None = field("memberId", default=None)
    name: PersonName = field("name")
    party: Party | None
    result_change: CoercedStr = field("resultChange", default=None)
    rank_order: int | None = field("rankOrder", default=None)
    votes: int
    vote_share: float | None = field("voteShare", default=None)


class ElectionResult(Schema):
    result: CoercedStr
    is_notional: bool = field("isNotional")
    electorate: int
    turnout: int
    majority: int
    election_name: CoercedStr = field("electionTitle", default=None)
    election_date: CoercedDate = field("electionDate")
    election_id: int = field("electionId")
    is_general_election: bool = field("isGeneralElection")
    candidates: list[ElectionCandidate]
    winning_party: Party | None = field("winningParty", default=None)
