"""

"""

import logging
from datetime import timedelta

from django.utils import timezone

from basetest.testcase import LocalTestCase
from social.models import Comment
from social.models.mixins import (
    DeletionPendingMixin,
    get_target_kwargs,
)
from social.models.token import UserToken
from social.tasks import delete_expired_models
from social.tests.util import (
    create_sample_comment,
    create_sample_usertoken,
)

log = logging.getLogger(__name__)


class TestDeleteExpiredTask(LocalTestCase):

    def test_delete_pending(self):
        DeletionPendingMixin.DELETION_PENDING_PERIOD_HOURS = 1
        now = timezone.now()

        target = create_sample_usertoken()
        token = create_sample_usertoken()

        pending_comment = create_sample_comment(target, token, 'hello pending')
        pending_comment.mark_pending_deletion()
        pending_comment.save()

        expired_comment = create_sample_comment(target, token, 'hello expired')
        expired_comment.mark_pending_deletion()
        expired_comment.deletion_requested_at = now - timedelta(hours=3)
        expired_comment.save()

        self.assertLengthEquals(Comment.objects.all(), 2)

        delete_expired_models()

        Comment.objects.get(text='hello pending')

        # Original comment should no longer exist, but an empty placeholder should have been created
        self.assertLengthEquals(Comment.objects.all(), 2)

        # Original has gone
        self.assertRaises(
            Comment.DoesNotExist,
            Comment.objects.get,
            text='hello expired',
        )

        # Placeholder exists
        Comment.objects.get(
            user=None, text='',
            **get_target_kwargs(target)
        )

    def tearDown(self) -> None:
        self.delete_instances_of(
            Comment,
            UserToken,
        )
