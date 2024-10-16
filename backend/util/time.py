import datetime
from typing import Optional

from django.utils import timezone


def get_now() -> datetime.datetime:
    return timezone.now()


def get_today() -> datetime.date:
    return get_now().date()


def coerce_timezone(dt) -> datetime.datetime:
    """
    Convert a date or naive datetime to an aware datetime.
    """
    if isinstance(dt, datetime.datetime):
        if timezone.is_aware(dt):
            return dt
        else:
            return timezone.make_aware(dt)

    elif isinstance(dt, datetime.date):
        return timezone.make_aware(datetime.datetime(dt.year, dt.month, dt.day))


def years_between(
    date_from: Optional[datetime.date],
    date_to: Optional[datetime.date],
) -> int:
    """Order is important! We will return zero if date_from is after date_to."""
    if not date_from or not date_to:
        return 0

    difference = date_to.year - date_from.year
    if date_to.month < date_from.month:
        difference = difference - 1
    elif date_to.month == date_from.month and date_to.day < date_from.day:
        difference = difference - 1

    return max(difference, 0)


def years_since(date: Optional[datetime.date], now=get_today) -> int:
    if callable(now):
        now = now()

    return years_between(date, now)


def is_anniversary(date: Optional[datetime.date], now=get_today) -> bool:
    if callable(now):
        now = now()

    if not date:
        return False

    return now.month == date.month and now.day == date.day


def year_only_date(year: int) -> datetime.date:
    """Some dates are only available as a year but we still want to treat them
    as datetime.date objects. Validation for datetime.date does not allow dates
    that don't fit on the calendar (we can't use the 0th or 32nd day, the 13th
    month, etc, etc) so we have to choose some date to represent a non-specific
    day of the year. We have chosen xmas day as an 'invalid' date as it seems
    perhaps the most reliably unlikely day for anything to happen in business,
    parliamentary or otherwise.
    """
    return datetime.date(year=year, month=12, day=25)


def in_range(
    date: datetime.date, start: Optional[datetime.date], end: Optional[datetime.date]
) -> bool:
    if start is None:
        return end is None or end > date
    if end is None:
        return start is None or start <= date

    return start <= date < end


def is_current(
    start: Optional[datetime.date], end: Optional[datetime.date], now=get_today
) -> bool:
    if callable(now):
        now = now()

    return in_range(now, start, end)
