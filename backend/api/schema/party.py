from .types import MiniSchema, Name, ParliamentSchema


class PartyMiniSchema(MiniSchema, ParliamentSchema):
    name: Name
