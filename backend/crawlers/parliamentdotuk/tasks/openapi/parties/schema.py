from crawlers.parliamentdotuk.tasks.types import field
from pydantic import BaseModel as Schema


class Party(Schema):
    parliamentdotuk: int = field("id")
    name: str | None = field("name", default=None)
    background_color: str | None = field("backgroundColor", default=None)
    foreground_color: str | None = field("foregroundColor", default=None)
    is_lords_main_party: bool = field("isLordsMainParty")
    is_lords_spiritual_party: bool = field("isLordsSpiritualParty")
    is_independent_party: bool = field("isIndependentParty")
