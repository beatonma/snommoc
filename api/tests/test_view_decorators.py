from django.urls import reverse

from api.models import (
    ApiKey,
    uuid,
    grant_read_snommoc_api,
)
from basetest.test_util import create_test_user
from basetest.testcase import LocalTestCase


class ApiKeyRequiredDecoratorTest(LocalTestCase):
    """Tests for @api_key_required View decorator."""

    def setUp(self):
        testuser = create_test_user()
        self.enabled_api_key = ApiKey.objects.create(user=testuser, enabled=True)
        self.disabled_api_key = ApiKey.objects.create(user=testuser, enabled=False)

        user_with_permission = create_test_user(
            username="user_with_permission",
            password="123456@abcdef",
            email="testuser2@snommoc.org",
        )
        grant_read_snommoc_api(user_with_permission)

    def assert_status_with_args(self, params, expected_status: int):
        response = self.client.get(reverse("decorator_test_view"), data=params)
        self.assertEqual(response.status_code, expected_status)

    def test_with_no_key__returns_http400(self):
        self.assert_status_with_args(params={}, expected_status=400)

    def test_with_invalid_key__returns_http403(self):
        self.assert_status_with_args(
            params={"key": "some-invalid-key"}, expected_status=403
        )

    def test_with_incorrect_key__returns_http403(self):
        self.assert_status_with_args(params={"key": uuid.uuid4()}, expected_status=403)

    def test_with_correct_key__returns_http200(self):
        self.assert_status_with_args(
            params={"key": self.enabled_api_key.key}, expected_status=200
        )

    def test_with_correct_but_disabled_key__returns_http403(self):
        self.assert_status_with_args(
            params={"key": self.disabled_api_key.key}, expected_status=403
        )

    def test_with_unknown_param__returns_http400(self):
        self.assert_status_with_args(
            params={"guessed_param": self.enabled_api_key}, expected_status=400
        )

    def test_user_has_permission(self):
        self.client.login(username="user_with_permission", password="123456@abcdef")
        response = self.client.get(reverse("decorator_test_view"), data={})
        self.assertEqual(response.status_code, 200)
