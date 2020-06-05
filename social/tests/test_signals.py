"""

"""

import logging
import uuid

from django.conf import settings
from django.contrib.auth.models import User

from basetest.test_util import create_test_user
from basetest.testcase import LocalTestCase
from social.models.token import (
    SignInServiceProvider,
    UserToken,
)

log = logging.getLogger(__name__)


class SignalTest(LocalTestCase):
    """Social signals tests."""
    def test_create_usertoken_on_user_created_is_correct(self):

        create_test_user()

        self.assertEqual(SignInServiceProvider.objects.first().name, 'snommoc.org')
        token = UserToken.objects.first()
        self.assertEqual(token.username, 'testuser')

    def tearDown(self) -> None:
        self.delete_instances_of(
            SignInServiceProvider,
            User,
            UserToken,
        )
