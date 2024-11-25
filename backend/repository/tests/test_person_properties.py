from datetime import date, datetime
from unittest.mock import patch

from basetest.testcase import LocalTestCase
from repository.models import House
from repository.models.person import Person
from repository.tests import values


class PersonPropertyTests(LocalTestCase):
    """Ensure that @property values on Person model are correct."""

    def test_person_age(self):
        living_person = Person(
            name=values.EXAMPLE_NAME,
            date_of_birth=date(1973, 6, 10),
        )

        dead_person = Person(
            name=values.EXAMPLE_NAME,
            date_of_birth=date(1973, 6, 10),
            date_of_death=date(2011, 5, 1),
        )

        with patch("util.time.timezone") as mock_time:
            mock_time.now = lambda: datetime(2021, 3, 5, 11, 13, 17)

            self.assertEqual(living_person.age(), 47)
            self.assertEqual(dead_person.age(), 37)

    def tearDown(self) -> None:
        self.delete_instances_of(
            House,
        )
