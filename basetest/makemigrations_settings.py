"""Simple configuration to allow makemigrations to run in a sandbox for testing."""

import os
import uuid
from snommoc.installed_apps import INSTALLED_APPS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-spec',
    '--spec-color',
    '--logging-clear-handlers',
    '--traverse-namespace',  # Required since Python 3.8
]

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'some-test-key'

INSTALLED_APPS += []

MIDDLEWARE = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

LANGUAGE_CODE = 'en-gb'

TEST_API_KEY = uuid.uuid4()
HTTP_REQUEST_HEADERS = {}
