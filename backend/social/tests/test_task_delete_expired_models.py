from datetime import timedelta

from social.models import Comment
from social.models.mixins import (
    DeletionPendingMixin,
    get_target_kwargs,
)
from social.tasks import delete_expired_models
from social.tests.testcase import SocialTestCase
from social.tests.util import (
    create_sample_comment,
    create_sample_usertoken,
)
from util.time import get_now


class TestDeleteExpiredTask(SocialTestCase):
    def test_delete_pending(self):
        DeletionPendingMixin.DELETION_PENDING_PERIOD_HOURS = 1
        now = get_now()

        target = create_sample_usertoken()
        token = create_sample_usertoken()

        pending_comment = create_sample_comment(target, token, "hello pending")
        pending_comment.mark_pending_deletion()
        pending_comment.save()

        expired_comment = create_sample_comment(target, token, "hello expired")
        expired_comment.mark_pending_deletion()
        expired_comment.deletion_requested_at = now - timedelta(hours=3)
        expired_comment.save()

        self.assertLengthEquals(Comment.objects.all(), 2)

        delete_expired_models()

        Comment.objects.get(text="hello pending")

        # Original comment should no longer exist, but an empty placeholder should have been created
        self.assertLengthEquals(Comment.objects.all(), 2)

        # Original has gone
        self.assertRaises(
            Comment.DoesNotExist,
            Comment.objects.get,
            text="hello expired",
        )

        # Placeholder exists
        Comment.objects.get(user=None, text="", **get_target_kwargs(target))

    # def tearDown(self) -> None:
    #     self.delete_instances_of(
    #         Comment,
    #         Comment,
    #         UserToken,
    #     )
