from datetime import date

from api.schema.types import Name, ParliamentSchema, field
from ninja import Schema

__all__ = [
    "ElectionSchema",
]


class ElectionSchema(ParliamentSchema, Schema):
    name: Name
    date: date | None
    election_type: str | None = field("election_type.name", default=None)
