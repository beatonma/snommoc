"""

"""
import datetime
import logging

from basetest.testcase import LocalTestCase
from repository.models import House
from repository.models.houses import (
    HOUSE_OF_COMMONS,
    HOUSE_OF_LORDS,
)
from repository.models.person import Person
from repository.tests import values

log = logging.getLogger(__name__)


class PersonPropertyTests(LocalTestCase):
    """Ensure that @property values on Person model are correct."""
    def test_person_age(self):
        living_person = Person(
            name=values.EXAMPLE_NAME,
            date_of_birth=datetime.date(year=1973, month=6, day=10)
        )
        self.assertEqual(living_person.age, 46)

        dead_person = Person(
            name=values.EXAMPLE_NAME,
            date_of_birth=datetime.date(year=1973, month=6, day=10),
            date_of_death=datetime.date(year=2011, month=5, day=1)
        )
        self.assertEqual(dead_person.age, 37)

    def test_person_is_mp(self):
        commons = House.objects.create(name=HOUSE_OF_COMMONS)
        lords = House.objects.create(name=HOUSE_OF_LORDS)
        commons.save()
        lords.save()

        inactive_mp = Person(
            name=values.EXAMPLE_NAME,
            active=False,
            house=commons
        )
        self.assertFalse(inactive_mp.is_mp)

        inactive_lord = Person(
            name=values.EXAMPLE_NAME,
            active=False,
            house=lords
        )
        self.assertFalse(inactive_lord.is_mp)

        active_lord = Person(
            name=values.EXAMPLE_NAME,
            active=True,
            house=lords
        )
        self.assertFalse(active_lord.is_mp)

        active_mp = Person(
            name=values.EXAMPLE_NAME,
            active=True,
            house=commons
        )
        self.assertTrue(active_mp.is_mp)

    def test_person_is_lord(self):
        commons = House.objects.create(name=HOUSE_OF_COMMONS)
        lords = House.objects.create(name=HOUSE_OF_LORDS)
        commons.save()
        lords.save()

        inactive_mp = Person(
            name=values.EXAMPLE_NAME,
            active=False,
            house=commons
        )
        self.assertFalse(inactive_mp.is_lord)

        inactive_lord = Person(
            name=values.EXAMPLE_NAME,
            active=False,
            house=lords
        )
        self.assertFalse(inactive_lord.is_lord)

        active_lord = Person(
            name=values.EXAMPLE_NAME,
            active=True,
            house=lords
        )
        self.assertTrue(active_lord.is_lord)

        active_mp = Person(
            name=values.EXAMPLE_NAME,
            active=True,
            house=commons
        )
        self.assertFalse(active_mp.is_lord)
