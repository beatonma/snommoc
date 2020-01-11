"""

"""
import datetime
import logging

log = logging.getLogger(__name__)


def years_since(date: datetime.date, now=datetime.datetime.now()) -> int:
    difference = now.year - date.year
    if now.month < date.month:
        difference = difference - 1
    elif now.month == date.month and now.day < date.day:
        difference = difference - 1

    return max(difference, 0)


def is_anniversary(date: datetime.date, now=datetime.datetime.now()) -> int:
    return now.month == date.month and now.day == date.day
