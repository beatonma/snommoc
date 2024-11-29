from crawlers.parliamentdotuk.tasks.types import Color, StringOrNone, field
from pydantic import BaseModel as Schema


class Party(Schema):
    parliamentdotuk: int = field("id")
    name: StringOrNone
    background_color: Color = field("backgroundColour", default=None)
    foreground_color: Color = field("foregroundColour", default=None)
    is_independent_party: bool = field("isIndependentParty")
