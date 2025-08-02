from datetime import date

from ninja import Schema

from api.schema.types import AdministrativeName, ParliamentSchema, field

__all__ = [
    "ElectionSchema",
]


class ElectionSchema(ParliamentSchema, Schema):
    name: AdministrativeName
    date: date | None
    election_type: str | None = field("election_type.name", default=None)
