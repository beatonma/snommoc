from crawlers.parliamentdotuk.tasks.types import field
from crawlers.types import NullableString
from pydantic import BaseModel as Schema

from .types import NestedDate, NestedValue, ParliamentId


class Constituency(Schema):
    parliamentdotuk: ParliamentId = field("_about")
    name: NestedValue[str] = field("label")
    os_name: NullableString = field("osName")
    gss_code: NullableString = field("gssCode")
    started_date: NestedDate = field("startedDate")
    ended_date: NestedDate | None = field("endedDate", default=None)
    type: NullableString = field("constituencyType", default=None)
