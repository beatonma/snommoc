from datetime import date

from .election import ElectionSchema
from .types import FullSchema, MiniSchema, Name, ParliamentSchema


class ConstituencyMiniSchema(MiniSchema, ParliamentSchema):
    name: Name


class HistoricalConstituencySchema(FullSchema):
    constituency: ConstituencyMiniSchema
    election: ElectionSchema
    start: date
    end: date | None
