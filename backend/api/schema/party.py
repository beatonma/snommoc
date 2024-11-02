from api.schema.types import FullSchema, Name, ParliamentSchema, Url, WikipediaPath

__all__ = [
    "PartyFullSchema",
]


class PartyFullSchema(FullSchema, ParliamentSchema):
    name: Name
    short_name: Name | None
    long_name: Name | None
    homepage: Url | None
    year_founded: int | None
    wikipedia: WikipediaPath | None
