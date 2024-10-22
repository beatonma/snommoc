import enum
from typing import Annotated

from ninja import Schema as NinjaSchema
from pydantic import BaseModel as Schema
from pydantic import BeforeValidator, Field

from . import types


class Session(Schema):
    name: str
    parliamentdotuk: types.ParliamentId | None


"""
LDA API structure:
[
    "2017/19",  # name
    "http://data.parliament.uk/resources/730830"  # number at the end is parliamentdotuk ID
]
"""
type SessionType = Annotated[
    Session,
    BeforeValidator(
        lambda obj: Session(
            name=obj[0], parliamentdotuk=obj[1] if len(obj) > 1 else None
        )
    ),
]


class VoteType(enum.StrEnum):
    AyeVote = "AyeVote"
    NoVote = "NoVote"
    Abstains = "Abstains"
    DidNotVote = "DidNotVote"
    SuspendedOrExpelledVote = "SuspendedOrExpelledVote"


"""
LDA API structure: "http://data.parliament.uk/schema/parl#AyeVote" 
"""
type VoteTypeType = Annotated[VoteType, BeforeValidator(lambda url: url.split("#")[-1])]


"""
LDA API structure:
[
    {
        "_about": "http://data.parliament.uk/members/4852",  # number at the end is parliamentdotuk ID
        "label": {
            "_value": "Biography information for Robert Largan"
        }
    }
]
"""
type VoteMemberId = Annotated[
    types.ParliamentId, BeforeValidator(lambda obj: obj[0]["_about"])
]


class Vote(NinjaSchema):
    member_parliamentdotuk: VoteMemberId = Field(validation_alias="member")
    type: VoteTypeType


class CommonsDivisionItem(Schema):
    parliamentdotuk: types.ParliamentId = Field(validation_alias="_about")


class CommonsDivision(Schema):
    parliamentdotuk: types.ParliamentId = Field(validation_alias="_about")
    date: types.NestedDate
    title: str
    uin: str
    session: SessionType
    division_number: int = Field(validation_alias="divisionNumber")
    deferred_vote: bool = Field(validation_alias="DeferredVote")
    abstentions: types.VoteCount = Field(validation_alias="AbstainCount")
    ayes: types.VoteCount = Field(validation_alias="AyesCount")
    noes: types.VoteCount = Field(validation_alias="Noesvotecount")
    did_not_vote: types.VoteCount = Field(validation_alias="Didnotvotecount")
    non_eligible: types.VoteCount = Field(validation_alias="Noneligiblecount")
    errors: types.VoteCount = Field(validation_alias="Errorvotecount")
    suspended_or_expelled: types.VoteCount = Field(
        validation_alias="Suspendedorexpelledvotescount"
    )
    votes: list[Vote] = Field(validation_alias="vote")
