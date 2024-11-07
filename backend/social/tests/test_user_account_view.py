"""
Tests for user account management.
"""

import json
import uuid
from typing import List

from api import status
from basetest.testcase import LocalTestCase
from django.urls import reverse
from social.models.token import SignInServiceProvider, UsernameChanged, UserToken
from social.views import contract


class UserAccountViewTests(LocalTestCase):
    """Tests for user account management."""

    VIEW_NAME = "social-account-view"

    def setUp(self) -> None:
        valid_user_token = uuid.uuid4()
        self.valid_user_token = str(valid_user_token)
        self.valid_google_id = str(uuid.uuid4().hex)
        self.original_username = "useraccount-username"

        self.provider = SignInServiceProvider.objects.create(
            name="fake-provider",
        )

        UserToken.objects.create(
            provider=self.provider,
            provider_account_id=self.valid_google_id,
            token=valid_user_token,
            enabled=True,
            username=self.original_username,
        )

    def tearDown(self) -> None:
        self.delete_instances_of(
            UsernameChanged,
            SignInServiceProvider,
            UserToken,
        )


class UserAccountViewPostTests(UserAccountViewTests):
    """Tests for user-triggered account updates."""

    def _check_response_code(self, newname: str, expected_status_code: int):
        response = self.client.post(
            reverse(UserAccountViewTests.VIEW_NAME),
            json.dumps(
                {
                    contract.ACCOUNT_ACTION: contract.ACCOUNT_CHANGE_USERNAME,
                    contract.USER_TOKEN: self.valid_user_token,
                    contract.USER_NAME: self.original_username,
                    contract.ACCOUNT_NEW_USERNAME: newname,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, expected_status_code)

    def _check_all_response_code(self, names: List[str], expected_status_code: int):
        for name in names:
            self._check_response_code(name, expected_status_code)
            self.tearDown()
            self.setUp()

    def test_rename_account_with_valid_tokens_is_httpnocontent(self):
        self._check_response_code("rubik", status.HTTP_204_NO_CONTENT)

        self.assertRaises(
            UserToken.DoesNotExist,  # noqa
            UserToken.objects.get,
            username=self.original_username,
        )
        renamed: UserToken = UserToken.objects.get(token=self.valid_user_token)
        self.assertEqual(renamed.username, "rubik")

    def test_rename_account_creates_previoususername(self):
        self._check_response_code("kibur", status.HTTP_204_NO_CONTENT)

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
            status.HTTP_403_FORBIDDEN,
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
            status.HTTP_403_FORBIDDEN,
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
            status.HTTP_204_NO_CONTENT,
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
            status.HTTP_403_FORBIDDEN,
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
            status.HTTP_204_NO_CONTENT,
        )


class UserAccountViewDeleteTests(UserAccountViewTests):
    """Tests for user account deletion."""

    def test_delete_account_with_valid_tokens_is_httpaccepted(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps(
                {
                    contract.GOOGLE_TOKEN: self.valid_google_id,
                    contract.USER_TOKEN: self.valid_user_token,
                }
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_account_with_invalid_usertoken_returns_httpbadrequest(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps(
                {
                    contract.GOOGLE_TOKEN: str(uuid.uuid4().hex),
                    contract.USER_TOKEN: self.valid_user_token,
                }
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account_with_invalid_googletoken_returns_httpbadrequest(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps(
                {
                    contract.GOOGLE_TOKEN: self.valid_google_id,
                    contract.USER_TOKEN: str(uuid.uuid4()),
                }
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account_with_missing_googletoken_returns_httpunauthorized(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps(
                {
                    contract.USER_TOKEN: self.valid_user_token,
                }
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_account_with_missing_usertoken_returns_httpunauthorized(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps(
                {
                    contract.GOOGLE_TOKEN: self.valid_google_id,
                }
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_account_with_invalid_data_returns_httpbadrequest(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data={
                contract.GOOGLE_TOKEN: self.valid_google_id,
                contract.USER_TOKEN: self.valid_user_token,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account_with_nonexistent_account_returns_httpbadrequest(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data={
                contract.GOOGLE_TOKEN: str(uuid.uuid4().hex),
                contract.USER_TOKEN: str(uuid.uuid4().hex),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
