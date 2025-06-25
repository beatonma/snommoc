from datetime import date
from typing import Literal

from api.schema.includes import MemberMiniSchema, MinimalMemberSchema, PartyMiniSchema
from api.schema.types import ParliamentSchema, field
from ninja import Schema
from repository.models.houses import HouseType

__all__ = [
    "CommonsDivisionSchema",
    "LordsDivisionSchema",
    "VoteSchema",
    "DivisionVoteType",
]


type DivisionVoteType = Literal["aye", "no", "did_not_vote"]


class DivisionVoteMemberSchema(MinimalMemberSchema):
    party: PartyMiniSchema


class VoteSchema(Schema):
    person: DivisionVoteMemberSchema
    vote: DivisionVoteType = field("vote_type.name")

    @staticmethod
    def resolve_vote(obj) -> DivisionVoteType:
        vote_type = obj.vote_type.name
        if vote_type == "aye" or vote_type == "content":
            return "aye"
        if vote_type == "no" or vote_type == "not_content":
            return "no"
        return vote_type


class CommonsDivisionSchema(ParliamentSchema):
    title: str
    date: date
    house: HouseType
    is_passed: bool
    is_deferred_vote: bool
    ayes: int
    noes: int
    did_not_vote: int


class LordsDivisionSchema(ParliamentSchema):
    title: str
    date: date
    house: HouseType
    description: str | None = field("amendment_motion_notes")
    sponsor: MemberMiniSchema | None = field("sponsoring_member", default=None)
    is_passed: bool
    is_whipped_vote: bool = field("is_whipped")
    ayes: int
    noes: int
