"""

"""

import logging

from basetest.testcase import LocalTestCase
from social.models import (
    Comment,
    Vote,
)
from social.tests.util import (
    create_comment,
    create_usertoken,
    create_vote,
)

log = logging.getLogger(__name__)


SAMPLE_COMMENT_TEXT = [
    'This is an insightful comment.',
    'Very nuanced input.'
]


class AccountDeletionTest(LocalTestCase):
    """Tests for affected data when a UserToken is deleted."""

    def test_account_deletion_replaces_comments_with_empty_placeholders(self):
        target = create_usertoken()

        token = create_usertoken()
        another_token = create_usertoken()

        for text in SAMPLE_COMMENT_TEXT:
            create_comment(target, token, text)

        # Different user
        create_comment(target, another_token, SAMPLE_COMMENT_TEXT[0])

        self.assertLengthEquals(Comment.objects.all(), 3)

        token.delete()

        # Comments should be replaced by empty placeholders via signals.on_comment_deleted
        self.assertLengthEquals(Comment.objects.all(), 3)
        self.assertLengthEquals(Comment.objects.filter(user=None), 2)
        self.assertLengthEquals(Comment.objects.filter(text=''), 2)

    def test_account_deletion_also_deletes_votes_by_account(self):
        target = create_usertoken()

        token = create_usertoken()
        another_token = create_usertoken()

        create_vote(target, token, 'aye')
        create_vote(target, another_token, 'aye')

        self.assertLengthEquals(Vote.objects.all(), 2)

        token.delete()

        self.assertLengthEquals(Vote.objects.all(), 1)
