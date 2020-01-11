"""

"""
import datetime
import logging
from typing import Optional

from basetest.testcase import LocalTestCase
from repository.models.util import time as timeutil

log = logging.getLogger(__name__)


class UtilTests(LocalTestCase):
    """"""
    def test_years_since(self):
        now = datetime.date(year=2019, month=11, day=17)

        def _assert_years_since(date: Optional[datetime.date], expected: int):
            self.assertEqual(timeutil.years_since(date, now=now), expected)

        _assert_years_since(datetime.date(year=2019, month=10, day=17), 0)
        _assert_years_since(datetime.date(year=2019, month=11, day=14), 0)
        _assert_years_since(datetime.date(year=2018, month=10, day=17), 1)
        _assert_years_since(datetime.date(year=2018, month=12, day=15), 0)

        _assert_years_since(datetime.date(year=1973, month=6, day=10), 46)
        _assert_years_since(datetime.date(year=1973, month=11, day=17), 46)
        _assert_years_since(datetime.date(year=1973, month=11, day=28), 45)
        _assert_years_since(datetime.date(year=1973, month=12, day=8), 45)

        # Future dates should return zero, not negative values
        _assert_years_since(datetime.date(year=2020, month=11, day=18), 0)

        _assert_years_since(None, 0)

    def test_is_anniversary(self):
        now = datetime.date(year=2019, month=11, day=17)

        def _assert_is_anniversary(year, month, day):
            self.assertTrue(timeutil.is_anniversary(datetime.date(year=year, month=month, day=day), now))

        def _assert_is_not_anniversary(year, month, day):
            self.assertFalse(timeutil.is_anniversary(datetime.date(year=year, month=month, day=day), now))

        _assert_is_not_anniversary(year=2019, month=11, day=16)
        _assert_is_not_anniversary(year=2019, month=11, day=18)
        _assert_is_not_anniversary(year=2020, month=11, day=18)
        _assert_is_not_anniversary(year=2019, month=2, day=18)

        _assert_is_anniversary(year=2020, month=11, day=17)
        _assert_is_anniversary(year=2021, month=11, day=17)
        _assert_is_anniversary(year=2042, month=11, day=17)

        self.assertFalse(timeutil.is_anniversary(None, now))
