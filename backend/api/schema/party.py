from api.schema.types import FullSchema, Name, ParliamentSchema, Url, WikipediaPath
from ninja import Schema

__all__ = ["PartyFullSchema", "PartyThemeSchema"]


class PartyThemeSchema(Schema):
    primary: str
    on_primary: str
    accent: str
    on_accent: str


class PartyFullSchema(FullSchema, ParliamentSchema):
    name: Name
    short_name: Name | None
    long_name: Name | None
    homepage: Url | None
    year_founded: int | None
    wikipedia: WikipediaPath | None
    theme: PartyThemeSchema | None

    @staticmethod
    def resolve_theme(obj):
        try:
            return obj.theme
        except AttributeError:
            # One-to-one rel Does not exist
            pass
