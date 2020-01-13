"""

"""
import datetime
import logging

from basetest.testcase import LocalTestCase
from repository.models import Constituency
from repository.models.constituency import (
    get_constituency_for_date,
    get_current_constituency,
)

log = logging.getLogger(__name__)


class ConstituencyTests(LocalTestCase):
    """"""
    def setUp(self) -> None:
        Constituency.objects.create(
            parliamentdotuk=1,
            name='A',
            start=datetime.date(year=1952, month=3, day=17),
            end=datetime.date(year=1957, month=4, day=1)
        )

        Constituency.objects.create(
            parliamentdotuk=2,
            name='A',
            start=datetime.date(year=1957, month=4, day=2),
            end=datetime.date(year=1978, month=8, day=2),
        )

        Constituency.objects.create(
            parliamentdotuk=3,
            name='A',
            start=datetime.date(year=1978, month=8, day=2),
            end=datetime.date(year=2005, month=4, day=1),
        )

        Constituency.objects.create(
            parliamentdotuk=4,
            name='A',
            start=datetime.date(year=2005, month=4, day=2),
        )

        Constituency.objects.create(
            parliamentdotuk=5,
            name='A',
        )

        Constituency.objects.create(
            parliamentdotuk=6,
            name='B',
            start=datetime.date(year=1952, month=3, day=17),
            end=datetime.date(year=1957, month=4, day=1)
        )

        Constituency.objects.create(
            parliamentdotuk=7,
            name='B',
            start=datetime.date(year=1957, month=4, day=2),
            end=datetime.date(year=1978, month=8, day=2),
        )

        Constituency.objects.create(
            parliamentdotuk=8,
            name='B',
            start=datetime.date(year=1978, month=8, day=2),
            end=datetime.date(year=2005, month=4, day=1),
        )

        Constituency.objects.create(
            parliamentdotuk=9,
            name='B',
            start=datetime.date(year=2005, month=4, day=2),
            end=datetime.date(year=2008, month=5, day=15),
        )

        Constituency.objects.create(
            parliamentdotuk=10,
            name='C',
            start=datetime.date(year=2005, month=4, day=2),
        )

    def test_get_constituency_for_date(self):
        # Date is before our earliest constituency. Should return earliest available.
        c = get_constituency_for_date(
            name='A',
            date=datetime.date(year=1932, month=1, day=1))
        self.assertEqual(c.parliamentdotuk, 1)

        # Within range
        c = get_constituency_for_date(
            name='A',
            date=datetime.date(year=1953, month=1, day=1))
        self.assertEqual(c.parliamentdotuk, 1)

        # Within range
        c = get_constituency_for_date(
            name='A',
            date=datetime.date(year=1967, month=10, day=21))
        self.assertEqual(c.parliamentdotuk, 2)

        # Within range
        c = get_constituency_for_date(
            name='A',
            date=datetime.date(year=1998, month=2, day=19))
        self.assertEqual(c.parliamentdotuk, 3)

        # After most recent start which has no end (i.e. still active)
        c = get_constituency_for_date(
            name='A',
            date=datetime.date(year=2011, month=5, day=18))
        self.assertEqual(c.parliamentdotuk, 4)

        # After latest end. Should return latest available.
        c = get_constituency_for_date(
            name='B',
            date=datetime.date(year=2021, month=6, day=5)
        )
        self.assertEqual(c.parliamentdotuk, 9)

        # Only one result for C. Should be returned regardless of requested date.
        c = get_constituency_for_date(
            name='C',
            date=datetime.date(year=1902, month=1, day=1)
        )
        self.assertEqual(c.parliamentdotuk, 10)

        # Only one result for C, should be returned regardless of requested date.
        c = get_constituency_for_date(
            name='C',
            date=datetime.date(year=2101, month=1, day=1)
        )
        self.assertEqual(c.parliamentdotuk, 10)

    def test_get_current_constituency(self):
        # Most recent start does not have an end date so should be considered current.
        c = get_current_constituency('A')
        self.assertEqual(c.parliamentdotuk, 4)

        # Date is after our latest end date. Should return latest available.
        c = get_current_constituency('B')
        self.assertEqual(c.parliamentdotuk, 9)

    def tearDown(self) -> None:
        self.delete_instances_of(Constituency)
