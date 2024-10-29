"""Field types used in pydantic schemas."""

from datetime import date, datetime
from typing import Annotated, Any

from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_boolean,
    coerce_to_date,
    coerce_to_datetime,
    coerce_to_list,
    coerce_to_str,
)
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException
from pydantic import AfterValidator, AliasPath, BeforeValidator, Field
from pydantic_core import PydanticUndefined

PHONE_NUMBER_REGION = "GB"

type CoercedStr = Annotated[
    str | None,
    BeforeValidator(coerce_to_str),
    AfterValidator(lambda x: x.strip() if x else None),
]
type CoercedBool = Annotated[bool | None, BeforeValidator(coerce_to_boolean)]
type CoercedDate = Annotated[date | None, BeforeValidator(coerce_to_date)]
type CoercedDateTime = Annotated[datetime | None, BeforeValidator(coerce_to_datetime)]
type CoercedList[T] = Annotated[
    list[T],
    BeforeValidator(coerce_to_list),
    Field(default_factory=list),
]


def _coerce_phonenumber(obj: str | None) -> str | None:
    try:
        return str(PhoneNumber.from_string(obj, PHONE_NUMBER_REGION))
    except NumberParseException:
        return None


type CoercedPhoneNumber = Annotated[
    str | None,
    BeforeValidator(_coerce_phonenumber),
    Field(default=None),
]


def field(validation_alias: str, *, default: Any = PydanticUndefined):
    """Convenience function for fields with validation_alias set.

    `validation_alias` may use dotted notation to indicate that the target
    data is nested in other objects - this will be resolved using AliasPath."""
    if "." in validation_alias:
        validation_alias = AliasPath(*validation_alias.split("."))

    default_factory = PydanticUndefined
    if callable(default):
        default_factory = default
        default = PydanticUndefined

    return Field(
        default=default,
        default_factory=default_factory,
        validation_alias=validation_alias,
    )
