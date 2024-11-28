from datetime import date, datetime
from unittest.mock import patch

from basetest.testcase import LocalTestCase
from repository.tests.data.create import create_sample_person


class PersonPropertyTests(LocalTestCase):
    """Ensure that @property values on Person model are correct."""

    def test_person_age(self):
        living_person = create_sample_person(
            date_of_birth=date(1973, 6, 10),
        )

        dead_person = create_sample_person(
            date_of_birth=date(1973, 6, 10),
            date_of_death=date(2011, 5, 1),
        )

        with patch("util.time.timezone") as mock_time:
            mock_time.now = lambda: datetime(2021, 3, 5, 11, 13, 17)

            self.assertEqual(living_person.age(), 47)
            self.assertEqual(dead_person.age(), 37)
