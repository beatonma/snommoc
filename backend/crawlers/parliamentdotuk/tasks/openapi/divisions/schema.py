"""Viewmodels for parsing responses from Division OpenAPI endpoints."""

from crawlers.parliamentdotuk.tasks.types import CoercedDate, CoercedDateTime
from pydantic import BaseModel as Schema


class DivisionMember(Schema):
    """
    Schema definition: https://lordsvotes-api.parliament.uk/index.html#model-MemberViewModel
    """

    memberId: int
    name: str | None

    """Sortable name"""
    listAs: str | None

    """Type of Lord e.g. 'Life peer', 'Bishops'"""
    memberFrom: str | None
    party: str | None
    partyColour: str | None
    partyAbbreviation: str | None
    partyIsMainParty: bool


class LordsDivision(Schema):
    """
    Schema definition: https://lordsvotes-api.parliament.uk/index.html#model-DivisionViewModel
    """

    divisionId: int
    date: CoercedDate
    number: int
    notes: str | None
    title: str | None
    isWhipped: bool
    isGovernmentContent: bool
    authoritativeContentCount: int
    authoritativeNotContentCount: int
    divisionHadTellers: bool
    tellerContentCount: int
    tellerNotContentCount: int
    memberContentCount: int
    memberNotContentCount: int
    sponsoringMemberId: int | None
    isHouse: bool | None
    amendmentMotionNotes: str | None
    isGovernmentWin: bool | None
    remoteVotingStart: CoercedDateTime
    remoteVotingEnd: CoercedDateTime
    divisionWasExclusivelyRemote: bool
    contentTellers: list[DivisionMember] | None
    notContentTellers: list[DivisionMember] | None
    contents: list[DivisionMember] | None
    notContents: list[DivisionMember] | None
