from basetest.test_util import create_sample_user
from basetest.testcase import LocalTestCase
from social.models import Comment, OAuthToken
from social.models.token import UserToken
from social.tests.util import create_sample_comment, create_sample_usertoken
from util.time import get_now


class SocialSignalTest(LocalTestCase):
    """Social signals tests."""

    def test_create_usertoken_on_user_created_is_correct(self):
        create_sample_user(username="SocialSignalTest")

        self.assertEqual(OAuthToken.objects.first().provider, "snommoc")
        token = UserToken.objects.first()
        self.assertEqual(token.username, "SocialSignalTest")

    def test_create_placeholder_on_comment_deleted_is_correct(self):
        token = create_sample_usertoken(username="fred")
        target = create_sample_usertoken()

        created_at = get_now().replace(
            year=2019, month=2, day=25, hour=15, minute=32, second=1, microsecond=0
        )
        now = get_now()

        comment = create_sample_comment(
            target=target,
            user=token,
            text="Hello my name is fred",
            created_at=created_at,
            modified_at=created_at,
        )

        comment.delete()

        placeholder_comment: Comment = Comment.objects.first()
        self.assertIsNone(placeholder_comment.user)
        self.assertEqual(placeholder_comment.text, "")
        self.assertEqual(placeholder_comment.target, target)

        # Ensure modified_at has been set to current timestamp when the comment was deleted
        self.assertNotEqual(created_at, now)
        self.assertEqual(placeholder_comment.created_at, created_at)
        self.assertEqual(placeholder_comment.modified_at.date(), now.date())
