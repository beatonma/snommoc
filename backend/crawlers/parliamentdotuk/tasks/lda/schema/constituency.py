from crawlers.types import NullableString
from pydantic import BaseModel as Schema
from pydantic import Field

from .types import NestedDate, NestedValue, ParliamentId


class Constituency(Schema):
    parliamentdotuk: ParliamentId = Field(validation_alias="_about")
    name: NestedValue[str] = Field(validation_alias="label")
    os_name: NullableString = Field(validation_alias="osName")
    gss_code: NullableString = Field(validation_alias="gssCode")
    started_date: NestedDate = Field(validation_alias="startedDate")
    ended_date: NestedDate | None = Field(default=None, validation_alias="endedDate")
    type: NullableString = Field(default=None, validation_alias="constituencyType")
