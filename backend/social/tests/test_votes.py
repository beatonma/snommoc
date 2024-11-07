import uuid

from api import status
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction
from django.urls import reverse
from repository.models import Person
from social.models.votes import Vote
from social.tests.testcase import SocialTestCase
from social.tests.util import create_sample_usertoken
from social.views import contract


def _create_person_vote(user, vote_type, target_id=4837):
    Vote.objects.create(
        user=user,
        target_type=ContentType.objects.get_for_model(Person),
        target_id=target_id,
        vote_type=vote_type,
    )


VIEWNAME_CREATE_VOTE = "social_api-2.0:create_vote"
VIEWNAME_DELETE_VOTE = "social_api-2.0:delete_vote"

VOTE_TYPE_AYE = Vote.VoteTypeChoices.AYE
VOTE_TYPE_NO = Vote.VoteTypeChoices.NO


class VoteTests(SocialTestCase):
    """Social votes tests."""

    def setUp(self) -> None:
        self.valid_token = uuid.uuid4()

        self.target_person = Person.objects.create(
            parliamentdotuk=4837, name="Aaron Bell", active=True
        )

        Person.objects.create(parliamentdotuk=1423, name="Boris Johnson", active=True)

        self.valid_user = create_sample_usertoken(
            "VoteTests-username", self.valid_token
        )

    def post_json(self, data: dict):
        return self.client.post(
            reverse("social_api-2.0:create_vote"), data, content_type="application/json"
        )

    def test_post_vote_with_valid_user(self):
        response = self.post_json(
            {
                "token": self.valid_token,
                "vote": "aye",
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertLengthEquals(Vote.objects.all(), 1)

        # Ensure vote points to the correct target
        vote = Vote.objects.first()
        self.assertEqual(vote.target_id, 4837)
        self.assertEqual(vote.target_type, ContentType.objects.get_for_model(Person))
        self.assertEqual(vote.target, self.target_person)

    def test_post_vote_with_invalid_user(self):
        response = self.post_json(
            {
                "token": uuid.uuid4(),
                "vote": "aye",
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNoneCreated(Vote)

    def test_post_vote_with_no_user(self):
        response = self.post_json(
            {
                "vote": "aye",
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertNoneCreated(Vote)

    def test_post_vote_with_invalid_target(self):
        response = self.post_json(
            {
                "token": self.valid_token,
                "vote": "aye",
                "target": "person",
                "target_id": 3181,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNoneCreated(Vote)

    def test_post_vote_with_invalid_type(self):
        response = self.post_json(
            {
                "token": self.valid_token,
                "vote": "arbitrary invalid value",
                "target": "person",
                "target_id": 3181,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertNoneCreated(Vote)

    def test_votes_one_vote_per_user_per_target(self):
        """Ensure a user can only vote once for a given target object."""
        target_type = ContentType.objects.get_for_model(Person)

        Vote.objects.create(
            user=self.valid_user,
            target_type=target_type,
            target_id=4837,
            vote_type=VOTE_TYPE_AYE,
        )

        # Different user
        Vote.objects.create(
            user=create_sample_usertoken(),
            target_type=target_type,
            target_id=4837,
            vote_type=VOTE_TYPE_AYE,
        )

        # User duplicate same target
        with transaction.atomic():
            self.assertRaises(
                IntegrityError,
                lambda: Vote.objects.create(
                    user=self.valid_user,
                    target_type=target_type,
                    target_id=4837,
                    vote_type=VOTE_TYPE_NO,
                ),
            )

    def test_delete_vote(self):
        _create_person_vote(self.valid_user, VOTE_TYPE_AYE)
        _create_person_vote(self.valid_user, VOTE_TYPE_AYE, target_id=1423)
        _create_person_vote(create_sample_usertoken(), VOTE_TYPE_AYE)
        _create_person_vote(create_sample_usertoken(), VOTE_TYPE_AYE)
        _create_person_vote(create_sample_usertoken(), VOTE_TYPE_NO)
        _create_person_vote(create_sample_usertoken(), VOTE_TYPE_NO)

        self.assertLengthEquals(Vote.objects.all(), 6)
        self.assertLengthEquals(Vote.objects.filter(user=self.valid_user), 2)

        response = self.client.delete(
            reverse(VIEWNAME_DELETE_VOTE),
            content_type="application/json",
            data={
                "token": self.valid_token.hex,
                "target": "person",
                "target_id": 1423,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLengthEquals(Vote.objects.all(), 5)
        self.assertLengthEquals(Vote.objects.filter(user=self.valid_user), 1)

        vote: Vote = Vote.objects.filter(user=self.valid_user).first()
        self.assertEqual(vote.target, self.target_person)

    def tearDown(self) -> None:
        self.delete_instances_of(
            Person,
            ContentType,
            *SocialTestCase.social_models,
        )
