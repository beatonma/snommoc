"""Field types used in pydantic schemas."""

from datetime import date, datetime
from typing import Annotated

from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_date,
    coerce_to_datetime,
    coerce_to_list,
)
from pydantic import AliasPath, BeforeValidator, Field
from pydantic_core import PydanticUndefined

type CoercedBool = Annotated[bool, BeforeValidator(coerce_to_boolean)]
type CoercedDate = Annotated[date | None, BeforeValidator(coerce_to_date)]
type CoercedDateTime = Annotated[datetime | None, BeforeValidator(coerce_to_datetime)]
type CoercedList = Annotated[list, BeforeValidator(coerce_to_list)]


def field(validation_alias: str, default=PydanticUndefined):
    """Convenience function for fields with validation_alias set.

    `validation_alias` may use dotted notation to indicate that the target
    data is nested in other objects - this will be resolved using AliasPath."""
    if "." in validation_alias:
        validation_alias = AliasPath(*validation_alias.split("."))

    return Field(default=default, validation_alias=validation_alias)
