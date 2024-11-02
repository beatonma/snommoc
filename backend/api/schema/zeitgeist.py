from ninja import Schema

from .mini import BillMiniSchema, DivisionMiniSchema, MemberMiniSchema
from .types import Url

__all__ = [
    "ZeitgeistSchema",
]


class Motd(Schema):
    title: str | None
    description: str | None
    action_url: Url | None


class ZeitgeistItem[T: Schema](Schema):
    priority: int
    reason: str
    target: T


class ZeitgeistSchema(Schema):
    motd: list[Motd]
    people: list[ZeitgeistItem[MemberMiniSchema]]
    divisions: list[ZeitgeistItem[DivisionMiniSchema]]
    bills: list[ZeitgeistItem[BillMiniSchema]]
