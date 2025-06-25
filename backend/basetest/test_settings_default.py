import uuid
from datetime import timedelta

import util.settings_contract as contract
from snommoc.settings import DATABASES, INSTALLED_APPS, MIDDLEWARE, ROOT_URLCONF  # noqa

TEST_RUNNER = "basetest.runner.PytestTestRunner"

ALLOWED_HOSTS = ["localhost"]
ADMIN_URL = "/test-admin/"
DASHBOARD_URL = "/test-dashboard/"
SECRET_KEY = "some-test-key"

DATABASES = {
    "default": {
        **DATABASES["default"],
        "NAME": "pytest",
    }
}
CACHES = {
    "default": {
        "BACKEND": "basetest.cache.DummyRedisCache",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

TEST_API_KEY = uuid.uuid4()
HTTP_REQUEST_HEADERS = {}
HTTP_REQUEST_HEADERS_JSON = {}


SNOMMOC = {
    contract.SOCIAL: {
        # Account name will be denied if it contains any of these substrings.
        contract.SOCIAL_USERNAME_BLOCKED_SUBSTRINGS: [
            "fallofmath",
            "admin",
        ],
        # Account name will be denied if it equals one of these strings.
        contract.SOCIAL_USERNAME_BLOCKED_EXACT: [
            "help",
            "info",
        ],
    },
    contract.CACHE: {
        contract.CACHE_CRAWLER_TTL: int(timedelta(days=10_000).total_seconds()),
        contract.CACHE_WIKI_TTL: int(timedelta(days=5).total_seconds()),
        contract.CRAWLER_CACHE_ROOT: "/tmp/snommoc/test/crawler_cache/",
    },
}

G_CLIENT_ID = "localhost"
