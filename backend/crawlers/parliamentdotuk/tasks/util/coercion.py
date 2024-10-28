"""
Functions for retrieving a specific type of data from data of some other type.
"""

from datetime import date, datetime

import dateutil
from dateutil.parser import ParserError
from util.time import coerce_timezone, year_only_date


def coerce_to_list(obj) -> list:
    """Wrap the given object in a list if it is not already a list.

    Some API responses return a list or a single object. To avoid handling each
    case separately we use this function to make sure we always have a list.
    """
    if obj is None:
        return []
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]


def coerce_to_int(value, default=None) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def coerce_to_str(value, default=None) -> str | None:
    if value is None:
        return default
    else:
        return str(value)


def coerce_to_boolean(value, default=None) -> bool | None:
    if value is None:
        return default

    if isinstance(value, str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False

    return bool(value)


def coerce_to_date(value) -> date | None:
    try:
        return dateutil.parser.parse(value).date()
    except (AttributeError, OverflowError, ParserError, TypeError, ValueError):
        pass

    if isinstance(value, dict):
        try:
            # Default to xmas day - we will use this to assume the day/month
            # values are missing.
            year = coerce_to_int(value.get("Year"))
            month = coerce_to_int(value.get("Month"))
            day = coerce_to_int(value.get("Day"))
            if month is None or day is None:
                return year_only_date(year)
            else:
                return date(year=year, month=month, day=day)
        except (TypeError, ValueError):
            pass


def coerce_to_datetime(value) -> datetime | None:
    try:
        dt = dateutil.parser.parse(value)
        return coerce_timezone(dt)
    except (AttributeError, OverflowError, ParserError, TypeError, ValueError):
        pass
