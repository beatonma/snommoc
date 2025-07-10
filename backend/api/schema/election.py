from datetime import date

from api.schema.types import AdministrativeName, ParliamentSchema, field
from ninja import Schema

__all__ = [
    "ElectionSchema",
]


class ElectionSchema(ParliamentSchema, Schema):
    name: AdministrativeName
    date: date | None
    election_type: str | None = field("election_type.name", default=None)
