"""

"""
import logging

from basetest.testcase import LocalTestCase
from repository.models import (
    GovernmentPost,
    ParliamentaryPost,
    OppositionPost,
    Person,
    GovernmentPostMember,
    House,
)
from repository.models.posts import (
    get_current_post_for_person,
    ParliamentaryPostMember,
    OppositionPostMember,
)
from util.time import get_today

log = logging.getLogger(__name__)


class PostTests(LocalTestCase):
    def setUp(self) -> None:
        GovernmentPost.objects.create(
            name="governmental", hansard_name="governmental", parliamentdotuk=1234
        )
        ParliamentaryPost.objects.create(
            name="parliamentary", hansard_name="parliamentary", parliamentdotuk=2345
        )
        OppositionPost.objects.create(
            name="opposition", hansard_name="opposition", parliamentdotuk=3456
        )
        House.objects.create(name="Commons")

        Person.objects.create(
            parliamentdotuk=3,
            active=True,
            house_id=1,
            name="Mr Mp",
        )

    def test_get_current_post_for_person__governmental(self):
        person = Person.objects.first()
        GovernmentPostMember.objects.create(
            post_id=1234, person=person, start=get_today()
        )

        post = get_current_post_for_person(person)
        self.assertEqual(post.person, person)
        self.assertEqual(post.post.name, "governmental")

    def test_get_current_post_for_person__parliamentary(self):
        person = Person.objects.first()
        ParliamentaryPostMember.objects.create(
            post_id=2345, person=person, start=get_today()
        )

        post = get_current_post_for_person(person)
        self.assertEqual(post.person, person)
        self.assertEqual(post.post.name, "parliamentary")

    def test_get_current_post_for_person__opposition(self):
        person = Person.objects.first()
        OppositionPostMember.objects.create(
            post_id=3456, person=person, start=get_today()
        )

        post = get_current_post_for_person(person)
        self.assertEqual(post.person, person)
        self.assertEqual(post.post.name, "opposition")

    def test_get_current_post_for_person__any(self):
        person = Person.objects.first()
        GovernmentPostMember.objects.create(
            post_id=1234, person=person, start=get_today()
        )
        ParliamentaryPostMember.objects.create(
            post_id=1234, person=person, start=get_today()
        )
        OppositionPostMember.objects.create(
            post_id=1234, person=person, start=get_today()
        )

        post = get_current_post_for_person(person)
        self.assertIsNotNone(post)
        self.assertEqual(post.person, person)
        self.assertIn(post.post.name, ["governmental", "opposition", "parliamentary"])

    def tearDown(self) -> None:
        self.delete_instances_of(
            GovernmentPost,
            GovernmentPostMember,
            ParliamentaryPost,
            ParliamentaryPostMember,
            OppositionPost,
            OppositionPostMember,
            Person,
            House,
        )
