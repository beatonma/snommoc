from basetest.test_util import create_sample_user
from social.models import Comment
from social.models.token import (
    SignInServiceProvider,
    UserToken,
)
from social.tests.testcase import SocialTestCase
from social.tests.util import (
    create_sample_comment,
    create_sample_usertoken,
)
from util.time import get_now


class SocialSignalTest(SocialTestCase):
    """Social signals tests."""

    def test_create_usertoken_on_user_created_is_correct(self):
        create_sample_user(username="SocialSignalTest")

        self.assertEqual(SignInServiceProvider.objects.first().name, "snommoc.org")
        token = UserToken.objects.first()
        self.assertEqual(token.username, "SocialSignalTest")

    def test_create_placeholder_on_comment_deleted_is_correct(self):
        token = create_sample_usertoken(username="fred")
        target = create_sample_usertoken()

        created_on = get_now().replace(
            year=2019, month=2, day=25, hour=15, minute=32, second=1, microsecond=0
        )
        now = get_now()

        comment = create_sample_comment(
            target=target,
            user=token,
            text="Hello my name is fred",
            created_on=created_on,
            modified_on=created_on,
        )

        comment.delete()

        placeholder_comment: Comment = Comment.objects.first()
        self.assertIsNone(placeholder_comment.user)
        self.assertEqual(placeholder_comment.text, "")
        self.assertEqual(placeholder_comment.target, target)

        # Ensure modified_on has been set to current timestamp when the comment was deleted
        self.assertNotEqual(created_on, now)
        self.assertEqual(placeholder_comment.created_on, created_on)
        self.assertEqual(placeholder_comment.modified_on.date(), now.date())

    # def tearDown(self) -> None:
    #     self.delete_instances_of(
    #         ApiKey,
    #         Comment,
    #         SignInServiceProvider,
    #         User,
    #         UserToken,
    #     )
