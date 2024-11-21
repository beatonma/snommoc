from datetime import date

from basetest.testcase import LocalTestCase
from repository.models import Post, PostHolder
from repository.tests.data.create import create_sample_person


class PostTests(LocalTestCase):
    def setUp(self) -> None:
        self.governmental = Post.objects.create(
            type="governmental",
            name="governmental",
            hansard_name="governmental",
            parliamentdotuk=1234,
        )
        self.opposition = Post.objects.create(
            type="opposition",
            name="opposition",
            hansard_name="opposition",
            parliamentdotuk=3456,
        )
        self.other = Post.objects.create(
            type="other",
            name="other",
            hansard_name="parliamentary",
            parliamentdotuk=2345,
        )

        self.person = create_sample_person()

        # Unrelated data which should not be included in queries
        PostHolder.objects.create(
            post=self.governmental,
            person=create_sample_person(),
            start=date(2020, 1, 5),
        )

    def test_get_current_posts(self):
        PostHolder.objects.create(
            post=self.governmental,
            person=self.person,
            start=date(2020, 1, 5),
            end=date(2021, 3, 6),
        )

        self.assertQuerysetSize(self.person.current_posts(), 0)

        PostHolder.objects.create(
            post=self.opposition,
            person=self.person,
            start=date(2023, 1, 5),
        )

        PostHolder.objects.create(
            post=self.other,
            person=self.person,
            start=date(2023, 1, 5),
        )
        self.assertQuerysetSize(self.person.current_posts(), 2)
