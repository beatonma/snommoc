"""

"""
import datetime
import logging
from typing import Optional

log = logging.getLogger(__name__)


def years_since(date: Optional[datetime.date], now=datetime.datetime.now()) -> int:
    if not date:
        return 0

    difference = now.year - date.year
    if now.month < date.month:
        difference = difference - 1
    elif now.month == date.month and now.day < date.day:
        difference = difference - 1

    return max(difference, 0)


def is_anniversary(date: Optional[datetime.date], now=datetime.datetime.now()) -> bool:
    if not date:
        return False

    return now.month == date.month and now.day == date.day
