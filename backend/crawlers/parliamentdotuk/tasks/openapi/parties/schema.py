from crawlers.parliamentdotuk.tasks.types import CoercedColor, field
from pydantic import BaseModel as Schema


class Party(Schema):
    parliamentdotuk: int = field("id")
    name: str | None
    background_color: CoercedColor = field("backgroundColour", default=None)
    foreground_color: CoercedColor = field("foregroundColour", default=None)
    is_independent_party: bool = field("isIndependentParty")
