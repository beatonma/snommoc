"""
Tests for user account management.
"""
import json
import logging
import uuid

from django.urls import reverse
from rest_framework import status

from basetest.testcase import LocalTestCase
from social.models.token import (
    SignInServiceProvider,
    UserToken,
)
from social.views import contract

log = logging.getLogger(__name__)


class UserAccountViewTests(LocalTestCase):
    """Tests for user account management."""
    VIEW_NAME = 'social-account-view'


class UserAccountViewDeleteTests(UserAccountViewTests):
    """Tests for user account deletion."""

    def setUp(self) -> None:
        valid_user_token = uuid.uuid4()
        self.valid_user_token = str(valid_user_token)
        self.valid_google_id = str(uuid.uuid4().hex)

        self.provider = SignInServiceProvider.objects.create(
            name='fake-provider',
        )
        self.provider.save()

        UserToken.objects.create(
            provider=self.provider,
            provider_account_id=self.valid_google_id,
            token=valid_user_token,
            enabled=True,
            username='TestUser',
        ).save()

    def test_delete_account_with_valid_tokens_is_httpaccepted(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps({
                contract.GOOGLE_TOKEN: self.valid_google_id,
                contract.USER_TOKEN: self.valid_user_token,
            })
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_account_with_invalid_usertoken_returns_httpbadrequest(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps({
                contract.GOOGLE_TOKEN: str(uuid.uuid4().hex),
                contract.USER_TOKEN: self.valid_user_token,
            })
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account_with_invalid_googletoken_returns_httpbadrequest(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps({
                contract.GOOGLE_TOKEN: self.valid_google_id,
                contract.USER_TOKEN: str(uuid.uuid4()),
            })
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account_with_missing_googletoken_returns_httpunauthorized(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps({
                contract.USER_TOKEN: self.valid_user_token,
            })
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_account_with_missing_usertoken_returns_httpunauthorized(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data=json.dumps({
                contract.GOOGLE_TOKEN: self.valid_google_id,
            })
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_account_with_invalid_data_returns_httpbadrequest(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data={
                contract.GOOGLE_TOKEN: self.valid_google_id,
                contract.USER_TOKEN: self.valid_user_token,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account_with_nonexistent_account_returns_httpbadrequest(self):
        response = self.client.delete(
            reverse(UserAccountViewTests.VIEW_NAME),
            data={
                contract.GOOGLE_TOKEN: str(uuid.uuid4().hex),
                contract.USER_TOKEN: str(uuid.uuid4().hex),
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
