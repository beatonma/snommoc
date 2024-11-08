import uuid

from api import permissions
from api.models import ApiKey
from basetest.test_util import create_sample_user
from basetest.testcase import LocalTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from social.models.token import UserToken


class ApiKeyRequiredDecoratorTest(LocalTestCase):
    """Tests for @api_key_required View decorator."""

    def setUp(self) -> None:
        self.delete_instances_of(User)
        testuser = create_sample_user(username="aaaaaaaaa")
        self.enabled_api_key = ApiKey.objects.create(user=testuser, enabled=True)
        self.disabled_api_key = ApiKey.objects.create(user=testuser, enabled=False)

        user_with_permission = create_sample_user(
            username="user_with_permission",
            password="123456@abcdef",
            email="testuser2@snommoc.org",
        )
        permissions.grant_read_snommoc_api(user_with_permission)

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

    def tearDown(self) -> None:
        self.delete_instances_of(
            ApiKey,
            User,
            UserToken,
        )
