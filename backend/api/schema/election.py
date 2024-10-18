from datetime import date

from api.schema.types import Name, ParliamentSchema, alias
from ninja import Schema


class ElectionSchema(ParliamentSchema, Schema):
    name: Name
    date: date | None
    election_type: str = alias("election_type.name")
