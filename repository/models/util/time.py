"""

"""
import datetime
import logging
from typing import Optional

log = logging.getLogger(__name__)


def years_between(date_from: Optional[datetime.date], date_to: Optional[datetime.date]) -> int:
    """Order is important! We will return zero if date_from is after date_to."""
    if not date_from or not date_to:
        return 0

    difference = date_to.year - date_from.year
    if date_to.month < date_from.month:
        difference = difference - 1
    elif date_to.month == date_from.month and date_to.day < date_from.day:
        difference = difference - 1

    return max(difference, 0)


def years_since(date: Optional[datetime.date], now=datetime.datetime.now()) -> int:
    return years_between(date, now)


def is_anniversary(date: Optional[datetime.date], now=datetime.datetime.now()) -> bool:
    if not date:
        return False

    return now.month == date.month and now.day == date.day
