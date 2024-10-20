from datetime import date, datetime
from typing import Callable

from django.utils import timezone

type _DefaultDate = Callable[[], date] | date


def get_now() -> datetime:
    return timezone.now()


def get_today() -> date:
    return get_now().date()


def tzdatetime(
    year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0
) -> datetime:
    return timezone.make_aware(
        datetime(year, month, day, hour, minute, second, microsecond)
    )


def coerce_timezone(dt) -> datetime:
    """
    Convert a date or naive datetime to an aware datetime.
    """
    if isinstance(dt, datetime):
        if timezone.is_aware(dt):
            return dt
        else:
            return timezone.make_aware(dt)

    elif isinstance(dt, date):
        return tzdatetime(dt.year, dt.month, dt.day)


def years_between(
    date_from: date | None,
    date_to: date | None,
) -> int:
    """Order is important! We will return zero if date_from is after date_to."""
    if not date_from or not date_to:
        return 0

    difference = date_to.year - date_from.year
    if date_to.month < date_from.month:
        difference -= 1
    elif date_to.month == date_from.month and date_to.day < date_from.day:
        difference -= 1

    return max(difference, 0)


def years_since(dt: date | None, now: _DefaultDate = get_today) -> int:
    if callable(now):
        now = now()

    return years_between(dt, now)


def is_anniversary(dt: date | None, now: _DefaultDate = get_today) -> bool:
    if callable(now):
        now = now()

    if not dt:
        return False

    return now.month == dt.month and now.day == dt.day


def year_only_date(year: int) -> date:
    """Some dates are only available as a year but we still want to treat them
    as date objects. Validation for date does not allow dates
    that don't fit on the calendar (we can't use the 0th or 32nd day, the 13th
    month, etc, etc) so we have to choose some date to represent a non-specific
    day of the year. We have chosen xmas day as an 'invalid' date as it seems
    perhaps the most reliably unlikely day for anything to happen in business,
    parliamentary or otherwise.
    """
    return date(year=year, month=12, day=25)


def in_range(dt: date, start: date | None, end: date | None) -> bool:
    if start is None:
        return end is None or end > dt
    if end is None:
        return start is None or start <= dt

    return start <= dt < end


def is_current(
    start: date | None, end: date | None, now: _DefaultDate = get_today
) -> bool:
    if callable(now):
        now = now()

    return in_range(now, start, end)
