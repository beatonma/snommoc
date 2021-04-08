"""

"""

import logging

from django.contrib.auth.models import User
from django.utils import timezone

from basetest.test_util import create_test_user
from basetest.testcase import LocalTestCase
from social.models import Comment
from social.models.token import (
    SignInServiceProvider,
    UserToken,
)
from social.tests.util import (
    create_sample_comment,
    create_sample_usertoken,
)

log = logging.getLogger(__name__)


class SocialSignalTest(LocalTestCase):
    """Social signals tests."""
    def test_create_usertoken_on_user_created_is_correct(self):

        create_test_user()

        self.assertEqual(SignInServiceProvider.objects.first().name, 'snommoc.org')
        token = UserToken.objects.first()
        self.assertEqual(token.username, 'testuser')

    def test_create_placeholder_on_comment_deleted_is_correct(self):
        token = create_sample_usertoken(username='fred')
        target = create_sample_usertoken()

        created_on = timezone.now().replace(
            year=2019, month=2, day=25, hour=15, minute=32, second=1,
            microsecond=0
        )
        now = timezone.now()

        comment = create_sample_comment(
            target=target,
            user=token,
            text='Hello my name is fred',
            created_on=created_on,
            modified_on=created_on,
        )

        comment.delete()

        placeholder_comment: Comment = Comment.objects.first()
        self.assertIsNone(placeholder_comment.user)
        self.assertEqual(placeholder_comment.text, '')
        self.assertEqual(placeholder_comment.target, target)

        # Ensure modified_on has been set to current timestamp when the comment was deleted
        self.assertNotEqual(created_on, now)
        self.assertEqual(placeholder_comment.created_on, created_on)
        self.assertEqual(placeholder_comment.modified_on.date(), now.date())

    def tearDown(self) -> None:
        self.delete_instances_of(
            Comment,
            SignInServiceProvider,
            User,
            UserToken,
        )
