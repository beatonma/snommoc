"""
Tests for /all/ endpoint.
"""
import json
import logging
import uuid

from django.conf import settings
from django.urls import reverse

from basetest.testcase import LocalTestCase
from repository.models import Person
from social.models import (
    Comment,
    Vote,
    VoteType,
)
from social.models.mixins import get_target_kwargs
from social.models.token import UserToken
from social.tests.util import create_usertoken
from social.views import contract

log = logging.getLogger(__name__)


def _comment(user, target, text):
    comment = Comment.objects.create(
        user=user,
        **get_target_kwargs(target),
        text=text,
    )
    comment.save()
    return comment


def _vote(user, target, vote_type_name):
    vote_type, _ = VoteType.objects.get_or_create(name=vote_type_name)
    vote = Vote.objects.create(
        user=user,
        **get_target_kwargs(target),
        vote_type=vote_type,
    )
    vote.save()
    return vote


class GetSocialAllTests(LocalTestCase):
    """Tests for social content endpoint /all/"""

    VIEW_NAME = 'social-member-all'

    def setUp(self, *args, **kwargs) -> None:
        self.valid_token = uuid.uuid4()

        self.target_person_one, _ = Person.objects.get_or_create(
            parliamentdotuk=4837,
            name='Aaron Bell',
            active=True
        )

        self.target_person_two, _ = Person.objects.get_or_create(
            parliamentdotuk=1423,
            name='Boris Johnson',
            active=True
        )

        self.valid_user, _ = UserToken.objects.get_or_create(
            token=self.valid_token,
            username='testuser',
        )

    def test_get_all_empty(self):
        settings.DEBUG = True
        response = self.client.get(
            reverse(GetSocialAllTests.VIEW_NAME, kwargs={
                'pk': 1423,
            })
        )
        settings.DEBUG = False

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(response.content, {
            contract.TITLE: 'Boris Johnson',
            contract.COMMENTS: [],
            contract.VOTES: {},
            contract.VOTE_TYPE: None,
        })

    def test_get_all_with_content_no_user_token(self):
        _comment(self.valid_user, self.target_person_one, 'first comment')
        _comment(self.valid_user, self.target_person_one, 'second comment')
        _comment(create_usertoken(username='another_user'), self.target_person_one, 'third comment')
        _comment(self.valid_user, self.target_person_two, 'comment on different target!')

        # Votes for actual target
        _vote(self.valid_user, self.target_person_one, 'aye')
        _vote(create_usertoken(), self.target_person_one, 'aye')
        _vote(create_usertoken(), self.target_person_one, 'no')

        # Votes on different target
        _vote(self.valid_user, self.target_person_two, 'aye')
        _vote(create_usertoken(), self.target_person_two, 'no')
        _vote(create_usertoken(), self.target_person_two, 'no')

        # Disable @api_key_required
        settings.DEBUG = True
        response = self.client.get(
            reverse(GetSocialAllTests.VIEW_NAME, kwargs={
                'pk': 4837,
            })
        )
        settings.DEBUG = False

        self.assertEqual(response.status_code, 200)

        self.assertSocialDataEqual(response, {
            contract.TITLE: 'Aaron Bell',
            contract.VOTES: {
                'aye': 2,
                'no': 1,
            },
            contract.COMMENTS: [
                ['first comment', 'testuser'],
                ['second comment', 'testuser'],
                ['third comment', 'another_user'],
            ],
            contract.VOTE_TYPE: None,
        })

    def test_get_all_with_content_with_user_token(self):
        """If user has voted on the target then their vote_type should be included in response"""
        _comment(self.valid_user, self.target_person_one, 'first comment')
        _comment(self.valid_user, self.target_person_one, 'second comment')
        _comment(create_usertoken(username='another_user'), self.target_person_one, 'third comment')
        _comment(self.valid_user, self.target_person_two, 'comment on different target!')

        # Votes for actual target
        _vote(self.valid_user, self.target_person_one, 'aye')
        _vote(create_usertoken(), self.target_person_one, 'aye')
        _vote(create_usertoken(), self.target_person_one, 'no')

        # Votes on different target
        _vote(self.valid_user, self.target_person_two, 'aye')
        _vote(create_usertoken(), self.target_person_two, 'no')
        _vote(create_usertoken(), self.target_person_two, 'no')

        # Disable @api_key_required
        settings.DEBUG = True
        response = self.client.get(
            reverse(GetSocialAllTests.VIEW_NAME, kwargs={
                'pk': 4837,
            }),
            data={
                contract.USER_TOKEN: self.valid_token,
            }
        )
        settings.DEBUG = False

        self.assertEqual(response.status_code, 200)

        self.assertSocialDataEqual(response, {
            contract.TITLE: 'Aaron Bell',
            contract.VOTES: {
                'aye': 2,
                'no': 1,
            },
            contract.COMMENTS: [
                ['first comment', 'testuser'],
                ['second comment', 'testuser'],
                ['third comment', 'another_user'],
            ],
            contract.VOTE_TYPE: 'aye',
        })

    def tearDown(self) -> None:
        self.delete_instances_of(
            Comment,
            Person,
            UserToken,
            Vote,
            VoteType,
        )

    def assertSocialDataEqual(self, response, expected):
        """
        expected_comments should be a list of (comment_text, username) tuples.
        """

        data = json.loads(response.content)

        # Replace timestamped comments with (text,username) tuples.
        actual_comments = [(x[contract.COMMENT_TEXT], x[contract.USER_NAME]) for x in data.get(contract.COMMENTS)]
        data[contract.COMMENTS] = actual_comments

        self.assertJSONEqual(
            json.dumps(data),
            expected,
        )
