from typing import Annotated

from crawlers.parliamentdotuk.tasks.openapi.members.schema import MemberBasic
from crawlers.parliamentdotuk.tasks.openapi.parties.schema import Party
from crawlers.parliamentdotuk.tasks.types import (
    DateOrNone,
    PersonName,
    StringOrNone,
    field,
)
from pydantic import AfterValidator
from pydantic import BaseModel as Schema


class Constituency(Schema):
    parliamentdotuk: int = field("id")
    name: str
    start_date: DateOrNone = field("startDate")
    end_date: DateOrNone = field("endDate")
    member: MemberBasic | None = field("currentRepresentation.member.value")


class ConstituencyBoundary(Schema):
    geojson: StringOrNone = field("value", default=None)


class ElectionCandidate(Schema):
    parliamentdotuk: int | None = field("memberId", default=None)
    name: PersonName = field("name")
    party: Party | None
    result_change: StringOrNone = field("resultChange", default=None)
    rank_order: int | None = field("rankOrder", default=None)
    votes: int
    vote_share: float | None = field("voteShare", default=None)


def _result_description(value: str | None) -> str | None:
    lc = value.lower()
    if lc.endswith("hold"):
        return "hold"
    if lc.endswith("gain"):
        return "gain"
    return value


type ResultDescription = Annotated[StringOrNone, AfterValidator(_result_description)]


class ElectionResult(Schema):
    result: ResultDescription
    is_notional: bool = field("isNotional")
    electorate: int
    turnout: int
    majority: int
    election_name: StringOrNone = field("electionTitle", default=None)
    election_date: DateOrNone = field("electionDate")
    election_id: int = field("electionId")
    is_general_election: bool = field("isGeneralElection")
    candidates: list[ElectionCandidate]
    winning_party: Party | None = field("winningParty", default=None)
