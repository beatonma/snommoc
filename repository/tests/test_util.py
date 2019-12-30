"""

"""
import datetime
import logging

from basetest.testcase import LocalTestCase
from repository.models.util.time import years_since

log = logging.getLogger(__name__)


class UtilTests(LocalTestCase):
    """"""
    def test_years_since(self):
        now = datetime.date(year=2019, month=11, day=17)

        def _assert_years_since(date: datetime.date, expected: int):
            self.assertEqual(years_since(date, now=now), expected)

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
