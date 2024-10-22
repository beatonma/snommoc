from datetime import date, datetime
from typing import Annotated

from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_date,
    coerce_to_datetime,
    coerce_to_list,
)
from pydantic import BeforeValidator

type CoercedDate = Annotated[date, BeforeValidator(coerce_to_date)]
type CoercedDateTime = Annotated[datetime, BeforeValidator(coerce_to_datetime)]
type CoercedList = Annotated[list, BeforeValidator(coerce_to_list)]
