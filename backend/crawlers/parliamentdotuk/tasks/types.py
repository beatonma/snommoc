"""Field types used in pydantic schemas."""

from datetime import date, datetime
from typing import Annotated

from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_date,
    coerce_to_datetime,
    coerce_to_list,
)
from pydantic import BeforeValidator

type CoercedBool = Annotated[bool, BeforeValidator(coerce_to_boolean)]
type CoercedDate = Annotated[date | None, BeforeValidator(coerce_to_date)]
type CoercedDateTime = Annotated[datetime | None, BeforeValidator(coerce_to_datetime)]
type CoercedList = Annotated[list, BeforeValidator(coerce_to_list)]
