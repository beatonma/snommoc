import os
import uuid

from datetime import timedelta

import util.settings_contract as contract

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
NOSE_ARGS = [
    "--with-spec",
    "--spec-color",
    "--logging-clear-handlers",
    "--traverse-namespace",  # Required since Python 3.8
    "--exe",
]

ALLOWED_HOSTS = ["localhost"]

SECRET_KEY = "some-test-key"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
]

MIDDLEWARE = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.test.sqlite3",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEST_API_KEY = uuid.uuid4()
HTTP_REQUEST_HEADERS = {}
HTTP_REQUEST_HEADERS_JSON = {}


CRAWLER_CACHE_ROOT = os.path.join(BASE_DIR, "cache/")

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
    },
}
