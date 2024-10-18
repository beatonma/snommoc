from datetime import date, datetime
from typing import Annotated

from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_boolean,
    coerce_to_date,
    coerce_to_datetime,
    coerce_to_int,
    coerce_to_list,
    coerce_to_str,
)
from pydantic import BeforeValidator

type CoercedBool = Annotated[bool, BeforeValidator(coerce_to_boolean)]
type CoercedDate = Annotated[date, BeforeValidator(coerce_to_date)]
type CoercedDateTime = Annotated[datetime, BeforeValidator(coerce_to_datetime)]
type CoercedInt = Annotated[int, BeforeValidator(coerce_to_int)]
type CoercedList = Annotated[list, BeforeValidator(coerce_to_list)]
type CoercedStr = Annotated[str, BeforeValidator(coerce_to_str)]
