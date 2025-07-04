from datetime import date

from api.schema.includes import (BaseDivisionVote, IncludeHouse,
                                 MemberMiniSchema, MinimalMemberSchema,
                                 PartyMiniSchema)
from api.schema.types import ParliamentSchema, field

__all__ = [
    "CommonsDivisionSchema",
    "LordsDivisionSchema",
    "VoteWithPersonSchema",
]


class DivisionVoteMemberSchema(MinimalMemberSchema):
    party: PartyMiniSchema


class VoteWithPersonSchema(BaseDivisionVote):
    person: DivisionVoteMemberSchema


class CommonsDivisionSchema(IncludeHouse, ParliamentSchema):
    title: str
    date: date
    is_deferred_vote: bool
    is_passed: bool
    ayes: int
    noes: int
    did_not_vote: int


class LordsDivisionSchema(IncludeHouse, ParliamentSchema):
    title: str
    date: date
    description: str | None = field("amendment_motion_notes")
    sponsor: MemberMiniSchema | None = field("sponsoring_member", default=None)
    is_whipped_vote: bool = field("is_whipped")
    is_passed: bool
    ayes: int
    noes: int
