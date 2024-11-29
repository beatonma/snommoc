from typing import Annotated

from phonenumber_field.phonenumber import PhoneNumber as PhoneNumberField
from phonenumbers import NumberParseException
from pydantic import BeforeValidator, Field

from .common import StringOrNone

__all__ = [
    "PhoneNumber",
]

PHONE_NUMBER_REGION = "GB"


def _coerce_phonenumber(obj: str | None) -> str | None:
    try:
        parsed = PhoneNumberField.from_string(obj, PHONE_NUMBER_REGION)
        if parsed.is_valid():
            return parsed.as_national
    except NumberParseException:
        return None


type PhoneNumber = Annotated[
    StringOrNone,
    BeforeValidator(_coerce_phonenumber),
    Field(default=None),
]
