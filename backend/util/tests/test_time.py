from datetime import date, datetime
from typing import Optional

from basetest.testcase import SimpleTestCase
from dateutil import tz
from util import time as timeutil
from util.time import coerce_timezone


class TimeUtilTests(SimpleTestCase):
    """Tests for util.time functions."""

    def test_years_between(self):
        self.assertEqual(
            timeutil.years_between(
                date(year=2000, month=1, day=1), date(year=2001, month=1, day=1)
            ),
            1,
        )
        self.assertEqual(
            timeutil.years_between(
                date(year=2000, month=1, day=1), date(year=2000, month=12, day=31)
            ),
            0,
        )
        self.assertEqual(
            timeutil.years_between(
                date(year=2000, month=1, day=1), date(year=2001, month=12, day=31)
            ),
            1,
        )
        self.assertEqual(
            timeutil.years_between(
                date(year=2000, month=1, day=1), date(year=2005, month=4, day=16)
            ),
            5,
        )

        # If dates are in wrong order return 0, not a negative number or normalised positive.
        self.assertEqual(
            timeutil.years_between(
                date(year=2005, month=4, day=16), date(year=2000, month=1, day=1)
            ),
            0,
        )

    def test_years_since(self):
        now = date(year=2019, month=11, day=17)

        def _assert_years_since(date: Optional[datetime.date], expected: int):
            self.assertEqual(timeutil.years_since(date, now=now), expected)

        _assert_years_since(date(year=2019, month=10, day=17), 0)
        _assert_years_since(date(year=2019, month=11, day=14), 0)
        _assert_years_since(date(year=2018, month=10, day=17), 1)
        _assert_years_since(date(year=2018, month=12, day=15), 0)

        _assert_years_since(date(year=1973, month=6, day=10), 46)
        _assert_years_since(date(year=1973, month=11, day=17), 46)
        _assert_years_since(date(year=1973, month=11, day=28), 45)
        _assert_years_since(date(year=1973, month=12, day=8), 45)

        # Future dates should return zero, not negative values
        _assert_years_since(date(year=2020, month=11, day=18), 0)

        _assert_years_since(None, 0)

    def test_is_anniversary(self):
        now = date(year=2019, month=11, day=17)

        def _assert_is_anniversary(year, month, day):
            self.assertTrue(
                timeutil.is_anniversary(date(year=year, month=month, day=day), now)
            )

        def _assert_is_not_anniversary(year, month, day):
            self.assertFalse(
                timeutil.is_anniversary(date(year=year, month=month, day=day), now)
            )

        _assert_is_not_anniversary(year=2019, month=11, day=16)
        _assert_is_not_anniversary(year=2019, month=11, day=18)
        _assert_is_not_anniversary(year=2020, month=11, day=18)
        _assert_is_not_anniversary(year=2019, month=2, day=18)

        _assert_is_anniversary(year=2020, month=11, day=17)
        _assert_is_anniversary(year=2021, month=11, day=17)
        _assert_is_anniversary(year=2042, month=11, day=17)

        self.assertFalse(timeutil.is_anniversary(None, now))

    def test_in_range(self):
        now = date(year=2020, month=3, day=15)

        def _assert_in_range(
            start: Optional[datetime.date], end: Optional[datetime.date]
        ):
            self.assertTrue(timeutil.in_range(now, start, end))

        def _assert_not_in_range(
            start: Optional[datetime.date], end: Optional[datetime.date]
        ):
            self.assertFalse(timeutil.in_range(now, start, end))

        _assert_in_range(None, None)
        _assert_in_range(None, date(2021, 3, 15))

        _assert_in_range(date(2001, 4, 16), date(2032, 1, 24))

        _assert_not_in_range(now, now)
        _assert_in_range(now, None)
        _assert_not_in_range(None, now)

        _assert_not_in_range(date(2032, 1, 24), None)
        _assert_not_in_range(None, date(2001, 4, 16))

        _assert_not_in_range(date(2001, 4, 16), date(2003, 5, 17))
        _assert_not_in_range(date(2032, 1, 24), date(2078, 1, 12))

    def test_coerce_timezone(self):
        self.assertEqual(
            coerce_timezone(date(2021, 12, 13)),
            datetime(2021, 12, 13, tzinfo=tz.tzutc()),
        )

        self.assertEqual(
            coerce_timezone(datetime(2021, 11, 12)),
            datetime(2021, 11, 12, tzinfo=tz.tzutc()),
        )

        self.assertEqual(
            coerce_timezone(datetime(2021, 6, 7, 8, 9, 10)),
            datetime(2021, 6, 7, 8, 9, 10, tzinfo=tz.tzutc()),
        )
