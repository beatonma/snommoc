from functools import wraps

from django.http import HttpResponse
from django.views import View

from api import contract as api_contract
from api.models import ApiKey
from api.views.decorators.api_key_required import api_key_required
from basetest import test_settings_default
from basetest.test_util import create_test_user


class ExampleView(View):
    @api_key_required
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse("OK")


def with_api_key(f, key=test_settings_default.TEST_API_KEY, **kwargs):
    """Decorate TestCase setUp methods with @with_api_key.
    setUp will be called with a kwarg called 'query' which includes
    a key parameter for making test calls to the api."""

    @wraps(f)
    def create_test_api_key(testcase):
        ApiKey.objects.create(user=create_test_user(), enabled=True, key=key)
        f(
            testcase,
            query={
                api_contract.API_KEY: key,
            },
            **kwargs
        )

    return create_test_api_key
