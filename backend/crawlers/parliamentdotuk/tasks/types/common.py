import re
from datetime import date, datetime
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, Field

from .coercion import coerce_to_date, coerce_to_datetime, coerce_to_list, coerce_to_str

__all__ = [
    "StringOrNone",
    "StringOrNoneKeepBreaks",
    "DateOrNone",
    "DateTimeOrNone",
    "List",
]


type DateOrNone = Annotated[date | None, BeforeValidator(coerce_to_date)]
type DateTimeOrNone = Annotated[datetime | None, BeforeValidator(coerce_to_datetime)]
type List[T] = Annotated[
    list[T],
    BeforeValidator(coerce_to_list),
    Field(default_factory=list),
]


def _normalize_whitespace(text: str | None) -> str | None:
    if text is None:
        return None

    return re.sub(r"\s+", " ", text).strip()


type StringOrNone = Annotated[
    str | None,
    BeforeValidator(coerce_to_str),
    AfterValidator(_normalize_whitespace),
]


def _normalize_whitespace_keep_breaks(text: str | None) -> str | None:
    if text is None:
        return None

    # Collapse multiple spaces into one
    text = re.sub(r" +", " ", text)

    # Collapse multiple linebreak characters into a single \n
    text = re.sub(r"[\r\n]+", "\n", text)
    return text.strip()


type StringOrNoneKeepBreaks = Annotated[
    str | None,
    BeforeValidator(coerce_to_str),
    AfterValidator(_normalize_whitespace_keep_breaks),
]
