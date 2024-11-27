"""
Tests for user account management.
"""

import uuid
from typing import List

from api import status
from basetest.testcase import LocalTestCase
from social.models.token import UsernameChanged, UserToken
from social.tests import reverse_api
from social.tests.util import create_sample_usertoken

VIEWNAME_GET = reverse_api("get_account")
VIEWNAME_RENAME = reverse_api("rename_account")
VIEWNAME_DELETE = reverse_api("delete_account")


class UserAccountViewTests(LocalTestCase):
    """Tests for user account management."""

    def setUp(self) -> None:
        valid_user_token = uuid.uuid4()
        self.valid_user_token = str(valid_user_token)
        self.valid_google_id = str(uuid.uuid4().hex)
        self.original_username = "useraccount-username"

        create_sample_usertoken(
            username=self.original_username,
            token=valid_user_token,
            enabled=True,
        )

    def tearDown(self) -> None:
        UserToken.objects.all().delete()


class GetUserAccountTests(UserAccountViewTests):
    def test_get_account(self):
        response = self.client.get(
            VIEWNAME_GET,
            data={"token": self.valid_user_token},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), {"username": self.original_username})

    def test_get_invalid_account(self):
        response = self.client.get(
            VIEWNAME_GET,
            data={"token": uuid.uuid4().hex},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAccountViewPostTests(UserAccountViewTests):
    """Tests for user-triggered account updates."""

    def _check_response_code(self, newname: str, expected_status_code: int):
        response = self.client.post(
            VIEWNAME_RENAME,
            {
                "token": self.valid_user_token,
                "username": self.original_username,
                "new_username": newname,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, expected_status_code)

    def _check_all_response_code(self, names: List[str], expected_status_code: int):
        for name in names:
            self._check_response_code(name, expected_status_code)
            self.tearDown()
            self.setUp()

    def test_rename_account_with_valid_tokens(self):
        self._check_response_code("rubik", status.HTTP_200_OK)

        self.assertRaises(
            UserToken.DoesNotExist,  # noqa
            UserToken.objects.get,
            username=self.original_username,
        )
        renamed: UserToken = UserToken.objects.get(token=self.valid_user_token)
        self.assertEqual(renamed.username, "rubik")

    def test_rename_account_creates_previoususername(self):
        self._check_response_code("kibur", status.HTTP_200_OK)

        changed: UsernameChanged = UsernameChanged.objects.first()
        self.assertEqual(changed.new_name, "kibur")
        self.assertEqual(changed.previous_name, self.original_username)

    def test_rename_account_blocked_substrings_are_forbidden(self):
        # Blocked strings defined in settings.
        # Values used for testing can be found in basetest.test_settings_default

        self._check_all_response_code(
            [
                "fallofmath",
                "fffallofmath",
                "fallofmathh",
                "admin",
                "Admin",
                "admin-user",
                "administrator",
                "real-admin",
                "a-d-m-i-n",
                "Adm.i__n1",
            ],
            status.HTTP_400_BAD_REQUEST,
        )

    def test_rename_account_blocked_exact_strings_are_forbidden(self):
        # Blocked strings defined in settings.
        # Values used for testing can be found in basetest.test_settings_default
        self._check_all_response_code(
            [
                "help",
                "Help",
                "HELP",
                "info",
                # Names should also be blocked if they reduce to a blocked string
                # when removing numbers/other characters
                "h-e.lp",
                "I-nfo",
                "info1",
            ],
            status.HTTP_400_BAD_REQUEST,
        )

    def test_rename_account_blocked_exact_strings_as_substrings_are_accepted(self):
        # Blocked strings defined in settings.
        # Values used for testing can be found in basetest.test_settings_default
        self._check_all_response_code(
            [
                "helpful",
                "shhelp",
                "shelper",
                "info-rmer",
                "informatics",
                "abcinfo",
            ],
            status.HTTP_200_OK,
        )

    def test_rename_account_username_validation_is_correct(self):
        self._check_all_response_code(
            [
                "-myname",  # Starts with non-alphanumeric character
                ".m.n",  # Starts with non-alphanumeric character
                "myname-",  # Ends with non-alphanumeric character
                "my.name.",  # Ends with non-alphanumeric character
                "_myname_",  # Starts and ends with non-alphanumeric character
                "myn",  # Fewer than 4 characters
                "m.n",  # Fewer than 4 characters
                "12345678901234567",  # More that 16 characters
                "abcdefghijklmnopq",  # More that 16 characters
            ],
            status.HTTP_400_BAD_REQUEST,
        )

        self._check_all_response_code(
            [
                "MyName",  # Simple case
                "name",  # Minimum length (4 characters)
                "my.name",  # Dots, dashes, underscores allowed in middle
                "my_na-me",  # Dots, dashes, underscores allowed in middle
                "my-_.name",  # Dots, dashes, underscores allowed in middle
                "123my-Name456",  # Dots, dashes, underscores allowed in middle
                "1234567890123456",  # Maximum length (16 characters)
            ],
            status.HTTP_200_OK,
        )


class UserAccountViewDeleteTests(UserAccountViewTests):
    """Tests for user account deletion."""

    def test_delete_account_with_valid_token(self):
        response = self.client.delete(
            VIEWNAME_DELETE,
            data={
                "token": self.valid_user_token,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_account_with_missing_usertoken(self):
        response = self.client.delete(
            VIEWNAME_DELETE,
            data={},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_delete_account_with_nonexistent_account(self):
        response = self.client.delete(
            VIEWNAME_DELETE,
            data={
                "token": str(uuid.uuid4().hex),
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
