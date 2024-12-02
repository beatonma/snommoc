from datetime import date

from api.schema.includes import MemberMiniSchema, PartyMiniSchema
from api.schema.types import Name, ParliamentId, ParliamentSchema, field
from repository.models.houses import HouseType

__all__ = [
    "CommonsDivisionSchema",
    "LordsDivisionSchema",
]


class CommonsVoteSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = field("person.parliamentdotuk")
    name: Name = field("person.name")
    vote: str = field("vote_type.name")
    party: PartyMiniSchema = field("person.party")


class CommonsDivisionSchema(ParliamentSchema):
    title: str
    date: date
    house: HouseType
    is_passed: bool
    is_deferred_vote: bool
    ayes: int
    noes: int
    did_not_vote: int
    votes: list[CommonsVoteSchema]


class LordsVoteSchema(ParliamentSchema):
    parliamentdotuk: ParliamentId = field("person.parliamentdotuk")
    name: Name = field("person.name")
    vote: str = field("vote_type.name")
    party: PartyMiniSchema = field("person.party")


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
    votes: list[LordsVoteSchema] = field("votes")
