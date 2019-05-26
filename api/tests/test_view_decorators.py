from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from api.models import ApiKey, uuid


class ApiKeyRequiredDecoratorTest(TestCase):
    """Tests for @api_key_required View decorator."""
    def setUp(self):
        testuser = User.objects.create(
            username='testuser',
            password=uuid.uuid4(),
            email='testuser@snommoc.org'
        )
        testuser.save()
        self.enabled_api_key = ApiKey.objects.create(user=testuser, enabled=True)
        self.enabled_api_key.save()

        self.disabled_api_key = ApiKey.objects.create(user=testuser, enabled=False)
        self.disabled_api_key.save()

    def assert_status_with_args(self, params, expected_status: int):
        response = self.client.get(reverse('decorator_test_view'), data=params)
        self.assertEqual(expected_status, response.status_code)

    def test_with_no_key__returns_http400(self):
        self.assert_status_with_args(
            params={},
            expected_status=400)

    def test_with_invalid_key__returns_http403(self):
        self.assert_status_with_args(
            params={'key': 'some-invalid-key'},
            expected_status=403)

    def test_with_incorrect_key__returns_http403(self):
        self.assert_status_with_args(
            params={'key': uuid.uuid4()},
            expected_status=403)

    def test_with_correct_key__returns_http200(self):
        self.assert_status_with_args(
            params={'key': self.enabled_api_key.key},
            expected_status=200)

    def test_with_correct_but_disabled_key__returns_http403(self):
        self.assert_status_with_args(
            params={'key': self.disabled_api_key.key},
            expected_status=403)

    def test_with_unknown_param__returns_http400(self):
        self.assert_status_with_args(
            params={'guessed_param': self.enabled_api_key},
            expected_status=400
        )
