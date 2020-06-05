"""

"""
import json
import logging
import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status

from basetest.testcase import LocalTestCase
from repository.models import Person
from social.models.token import UserToken
from social.models.votes import (
    Vote,
    VoteType,
)
from social.tests.util import create_usertoken
from social.views import contract

log = logging.getLogger(__name__)


def _create_person_vote(user, vote_type):
    Vote.objects.create(
        user=user,
        target_type=ContentType.objects.get_for_model(Person),
        target_id=4837,
        vote_type=vote_type
    ).save()


class VoteTests(LocalTestCase):
    """Social votes tests."""
    VIEW_NAME = 'social-member-votes'

    def setUp(self) -> None:
        self.valid_token = uuid.uuid4()

        self.target_person = Person.objects.create(
            parliamentdotuk=4837,
            name='Aaron Bell',
            active=True
        )
        self.target_person.save()

        self.valid_user = create_usertoken('testuser', self.valid_token)

    def test_post_vote_with_valid_user(self):
        response = self.client.post(
            reverse(VoteTests.VIEW_NAME, kwargs={'pk': 4837}),
            {
                contract.USER_TOKEN: self.valid_token,
                contract.VOTE_TYPE: 'aye'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        VoteType.objects.get(name='aye')  # Ensure VoteType was created
        self.assertLengthEquals(Vote.objects.all(), 1)

    def test_post_vote_with_invalid_user(self):
        response = self.client.post(
            reverse(VoteTests.VIEW_NAME, kwargs={'pk': 4837}),
            {
                contract.USER_TOKEN: uuid.uuid4(),
                contract.VOTE_TYPE: 'aye'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNoneCreated(Vote)

    def test_post_vote_with_no_user(self):
        response = self.client.post(
            reverse(VoteTests.VIEW_NAME, kwargs={'pk': 4837}),
            {
                contract.VOTE_TYPE: 'aye'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNoneCreated(Vote)

    def test_post_vote_with_invalid_target(self):
        response = self.client.post(
            reverse(VoteTests.VIEW_NAME, kwargs={'pk': 3181}),
            {
                contract.USER_TOKEN: self.valid_token,
                contract.VOTE_TYPE: 'aye'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNoneCreated(Vote)

    def test_post_vote_with_invalid_type(self):
        response = self.client.post(
            reverse(VoteTests.VIEW_NAME, kwargs={'pk': 4837}),
            {
                contract.USER_TOKEN: self.valid_token,
                contract.VOTE_TYPE: 'a'*20,  # Too long
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNoneCreated(Vote)

    def test_votes_one_vote_per_user_per_target(self):
        """Ensure a user can only vote once for a given target object."""
        vote_type_aye = VoteType.objects.create(name='aye')
        vote_type_aye.save()

        vote_type_no = VoteType.objects.create(name='no')
        vote_type_no.save()

        Vote.objects.create(
            user=self.valid_user,
            target_type=ContentType.objects.get_for_model(Person),
            target_id=4837,
            vote_type=vote_type_aye,
        ).save()

        # Different user
        Vote.objects.create(
            user=create_usertoken(),
            target_type=ContentType.objects.get_for_model(Person),
            target_id=4837,
            vote_type=vote_type_aye,
        ).save()

        # User duplicate same target
        self.assertRaises(IntegrityError, lambda: Vote.objects.create(
            user=self.valid_user,
            target_type=ContentType.objects.get_for_model(Person),
            target_id=4837,
            vote_type=vote_type_no,
        ).save())

    def test_get_votes(self):
        vote_type_aye = VoteType.objects.create(name='aye')
        vote_type_no = VoteType.objects.create(name='no')
        vote_type_aye.save()
        vote_type_no.save()

        _create_person_vote(self.valid_user, vote_type_aye)
        _create_person_vote(create_usertoken(), vote_type_aye)
        _create_person_vote(create_usertoken(), vote_type_aye)
        _create_person_vote(create_usertoken(), vote_type_no)
        _create_person_vote(create_usertoken(), vote_type_no)

        # @api_key_required
        response = self.client.get(
            reverse(VoteTests.VIEW_NAME, kwargs={'pk': 4837}),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Disable @api_key_required
        settings.DEBUG = True
        response = self.client.get(
            reverse(VoteTests.VIEW_NAME, kwargs={'pk': 4837}),
        )
        settings.DEBUG = False

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)

        self.assertEqual(data['aye'], 3)
        self.assertEqual(data['no'], 2)

    def tearDown(self) -> None:
        self.delete_instances_of(
            Person,
            Vote,
            VoteType,
            ContentType,
            UserToken,
        )
