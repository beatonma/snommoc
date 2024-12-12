from datetime import date, datetime
from unittest.mock import patch

from basetest.testcase import DatabaseTestCase
from repository.models import Post, PostHolder
from repository.tests.data.create import create_sample_person


class PersonPropertyTests(DatabaseTestCase):
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

    def test_get_current_posts(self):
        governmental = Post.objects.create(
            type="governmental",
            name="governmental",
            hansard_name="governmental",
            parliamentdotuk=1234,
        )
        opposition = Post.objects.create(
            type="opposition",
            name="opposition",
            hansard_name="opposition",
            parliamentdotuk=3456,
        )
        other = Post.objects.create(
            type="other",
            name="other",
            hansard_name="parliamentary",
            parliamentdotuk=2345,
        )

        person = create_sample_person()

        # Unrelated data which should not be included in queries
        PostHolder.objects.create(
            post=governmental,
            person=create_sample_person(),
            start=date(2020, 1, 5),
        )

        PostHolder.objects.create(
            post=governmental,
            person=person,
            start=date(2020, 1, 5),
            end=date(2021, 3, 6),
        )

        self.assertQuerysetSize(person.current_posts(), 0)

        PostHolder.objects.create(
            post=opposition,
            person=person,
            start=date(2023, 1, 5),
        )

        PostHolder.objects.create(
            post=other,
            person=person,
            start=date(2023, 1, 5),
        )
        self.assertQuerysetSize(person.current_posts(), 2)
