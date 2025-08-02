from unittest.mock import patch

import google.oauth2.id_token

from basetest.testcase import DatabaseTestCase
from social.models import UserToken
from social.tests.util import reverse_api


def _patched_id_token(oauth_token: str, request, audience: str | None):
    return {
        "iss": "https://accounts.google.com",
        "sub": "1234567890",
        "aud": "localhost",
        "scope": "read write",
        "exp": 1635200000,
        "iat": 1635196400,
        "nbf": 1635196400,
        "jti": "abc123",
    }


class OAuthTests(DatabaseTestCase):
    def test_google_oauth_response(self):
        with patch.object(
            google.oauth2.id_token,
            "verify_oauth2_token",
            side_effect=_patched_id_token,
        ):
            response = self.client.post(
                reverse_api("verify_google_token"),
                data={"encoded_oauth_token": "abcdefghijklmnopqrstuvwxyz"},
                content_type="application/json",
            ).json()

        match response:
            case {
                "token": str(token),
                "username": str(username),
            }:
                # Confirm that UserToken object was created
                UserToken.objects.get(username=username, token=token)
            case _:
                raise AssertionError(f"Unexpected structure: {response}")
