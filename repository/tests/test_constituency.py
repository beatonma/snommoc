"""

"""
from datetime import date
import logging

from basetest.testcase import LocalTestCase
from repository.models import Constituency
from repository.models.constituency import (
    get_constituency_for_date,
    get_current_constituency,
    get_suggested_constituencies,
)
from repository.tests.data.sample_constituencies import create_sample_constituencies


log = logging.getLogger(__name__)


class ConstituencyTests(LocalTestCase):
    """ """

    def setUp(self) -> None:
        Constituency.objects.create(
            parliamentdotuk=1,
            name="A",
            start=date(year=1952, month=3, day=17),
            end=date(year=1957, month=4, day=1),
        )

        Constituency.objects.create(
            parliamentdotuk=2,
            name="A",
            start=date(year=1957, month=4, day=2),
            end=date(year=1978, month=8, day=2),
        )

        Constituency.objects.create(
            parliamentdotuk=3,
            name="A",
            start=date(year=1978, month=8, day=2),
            end=date(year=2005, month=4, day=1),
        )

        Constituency.objects.create(
            parliamentdotuk=4,
            name="A",
            start=date(year=2005, month=4, day=2),
        )

        Constituency.objects.create(
            parliamentdotuk=5,
            name="A",
        )

        Constituency.objects.create(
            parliamentdotuk=6,
            name="B",
            start=date(year=1952, month=3, day=17),
            end=date(year=1957, month=4, day=1),
        )

        Constituency.objects.create(
            parliamentdotuk=7,
            name="B",
            start=date(year=1957, month=4, day=2),
            end=date(year=1978, month=8, day=2),
        )

        Constituency.objects.create(
            parliamentdotuk=8,
            name="B",
            start=date(year=1978, month=8, day=2),
            end=date(year=2005, month=4, day=1),
        )

        Constituency.objects.create(
            parliamentdotuk=9,
            name="B",
            start=date(year=2005, month=4, day=2),
            end=date(year=2008, month=5, day=15),
        )

        Constituency.objects.create(
            parliamentdotuk=10,
            name="C",
            start=date(year=2005, month=4, day=2),
        )

        Constituency.objects.create(
            parliamentdotuk=11,
            name="D",
            start=None,
            end=None,
        )

    def test_get_constituency_for_date(self):
        # Date is before our earliest constituency. Should return earliest available.
        c = get_constituency_for_date(name="A", date=date(year=1932, month=1, day=1))
        self.assertEqual(c.parliamentdotuk, 1)

        # Within range
        c = get_constituency_for_date(name="A", date=date(year=1953, month=1, day=1))
        self.assertEqual(c.parliamentdotuk, 1)

        # Within range
        c = get_constituency_for_date(name="A", date=date(year=1967, month=10, day=21))
        self.assertEqual(c.parliamentdotuk, 2)

        # Within range
        c = get_constituency_for_date(name="A", date=date(year=1998, month=2, day=19))
        self.assertEqual(c.parliamentdotuk, 3)

        # After most recent start which has no end (i.e. still active)
        c = get_constituency_for_date(name="A", date=date(year=2011, month=5, day=18))
        self.assertEqual(c.parliamentdotuk, 4)

        # After latest end. Should return latest available.
        c = get_constituency_for_date(name="B", date=date(year=2021, month=6, day=5))
        self.assertEqual(c.parliamentdotuk, 9)

        # Only one result for C. Should be returned regardless of requested date.
        c = get_constituency_for_date(name="C", date=date(year=1902, month=1, day=1))
        self.assertEqual(c.parliamentdotuk, 10)

        # Only one result for C, should be returned regardless of requested date.
        c = get_constituency_for_date(name="C", date=date(year=2101, month=1, day=1))
        self.assertEqual(c.parliamentdotuk, 10)

        c = get_constituency_for_date("D", date=date(year=2101, month=1, day=1))
        self.assertEqual(c.parliamentdotuk, 11)

    def test_get_constituency_for_date_with_complex_names(self):
        """
        Ensure punctuation, &/and equivalency, etc.
        """
        create_sample_constituencies()

        c = get_constituency_for_date("Barnsley East & Mexborough", date(2001, 6, 1))
        self.assertEqual(c.parliamentdotuk, 143590)

        c = get_constituency_for_date("Barnsley East and Mexborough", date(2001, 6, 1))
        self.assertEqual(c.parliamentdotuk, 143590)

        c = get_constituency_for_date(
            "Tweeddale, Ettrick and Lauderdale", date(1995, 5, 16)
        )
        self.assertEqual(c.parliamentdotuk, 146426)

        c = get_constituency_for_date(
            "Tweeddale, Ettrick & Lauderdale", date(1995, 5, 16)
        )
        self.assertEqual(c.parliamentdotuk, 146426)

        c = get_constituency_for_date(
            "Ealing, Acton & Shepherd's Bush", date(2009, 5, 6)
        )
        self.assertEqual(c.parliamentdotuk, 144408)

        c = get_constituency_for_date(
            "Ealing, Acton and Shepherd's Bush", date(2009, 5, 6)
        )
        self.assertEqual(c.parliamentdotuk, 144408)

    def test_get_current_constituency(self):
        # Most recent start does not have an end date so should be considered current.
        c = get_current_constituency("A")
        self.assertEqual(c.parliamentdotuk, 4)

        # Date is after our latest end date. Should return latest available.
        c = get_current_constituency("B")
        self.assertEqual(c.parliamentdotuk, 9)

    def test_get_suggested_constituencies(self):
        create_sample_constituencies()

        suggestions = get_suggested_constituencies("aberdeen", date(1982, 3, 15))

        self.assertLengthEquals(suggestions, 2)
        self.assertTrue(Constituency(pk=143471, name="Aberdeen North") in suggestions)
        self.assertTrue(Constituency(pk=143477, name="Aberdeen South") in suggestions)

    def tearDown(self) -> None:
        self.delete_instances_of(Constituency)
