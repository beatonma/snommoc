"""Viewmodels for parsing responses from Division OpenAPI endpoints."""

from crawlers.parliamentdotuk.tasks.types import (
    DateOrNone,
    DateTimeOrNone,
    PersonName,
    SafeHtmlOrNone,
    StringOrNone,
    field,
)
from pydantic import BaseModel as Schema
from pydantic import model_validator


class Member:
    member_id: int
    name: str
    party: str | None


class LordsMember(Member, Schema):
    """
    Schema definition: https://lordsvotes-api.parliament.uk/index.html#model-MemberViewModel
    """

    member_id: int = field("memberId")
    name: PersonName

    """Sortable name"""
    list_as: StringOrNone = field("listAs", default=None)

    """Type of Lord e.g. 'Life peer', 'Bishops'"""
    member_from: StringOrNone = field("memberFrom", default=None)
    party: StringOrNone


class LordsDivision(Schema):
    """
    Schema definition: https://lordsvotes-api.parliament.uk/index.html#model-DivisionViewModel
    """

    division_id: int = field("divisionId")
    date: DateOrNone
    number: int
    notes: StringOrNone
    title: StringOrNone
    is_whipped: bool = field("isWhipped")
    is_government_content: bool = field("isGovernmentContent")
    authoritative_content_count: int = field("authoritativeContentCount")
    authoritative_not_content_count: int = field("authoritativeNotContentCount")
    division_had_tellers: bool = field("divisionHadTellers")
    teller_content_count: int = field("tellerContentCount")
    teller_not_content_count: int = field("tellerNotContentCount")
    member_content_count: int = field("memberContentCount")
    member_not_content_count: int = field("memberNotContentCount")
    sponsoring_member_id: int | None = field("sponsoringMemberId")
    is_house: bool | None = field("isHouse")
    amendment_motion_notes: SafeHtmlOrNone = field("amendmentMotionNotes")
    is_government_win: bool | None = field("isGovernmentWin")
    remote_voting_start: DateTimeOrNone = field("remoteVotingStart")
    remote_voting_end: DateTimeOrNone = field("remoteVotingEnd")
    division_was_exclusively_remote: bool = field("divisionWasExclusivelyRemote")
    content_tellers: list[LordsMember] | None = field("contentTellers")
    not_content_tellers: list[LordsMember] | None = field("notContentTellers")
    contents: list[LordsMember] | None
    not_contents: list[LordsMember] | None = field("notContents")


class CommonsDivisionItem(Schema):
    division_id: int = field("DivisionId")


class CommonsMember(Member, Schema):
    member_id: int = field("MemberId")
    name: PersonName = field("Name")
    party: StringOrNone  # See validate_party method
    constituency: StringOrNone = field("MemberFrom")

    @model_validator(mode="before")
    @classmethod
    def validate_party(cls, obj):
        """Combine Party and SubParty fields."""
        party = obj.get("Party")
        sub_party = obj.get("SubParty")
        obj["party"] = f"{party} {sub_party}" if sub_party else party

        return obj


class CommonsDivision(Schema):
    division_id: int = field("DivisionId")
    date: DateOrNone = field("Date")
    publication_updated: DateTimeOrNone = field("PublicationUpdated")
    number: int = field("Number")
    is_deferred: bool = field("IsDeferred")
    title: StringOrNone = field("Title")
    friendly_title: StringOrNone = field("FriendlyTitle")
    friendly_description: StringOrNone = field("FriendlyDescription")
    aye_count: int = field("AyeCount")
    no_count: int = field("NoCount")
    aye_tellers: list[CommonsMember] = field("AyeTellers")
    no_tellers: list[CommonsMember] = field("NoTellers")
    ayes: list[CommonsMember] = field("Ayes")
    noes: list[CommonsMember] = field("Noes")
    did_not_vote: list[CommonsMember] = field("NoVoteRecorded")
