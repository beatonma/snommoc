import os
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-spec',
    '--spec-color',
    '--logging-clear-handlers',
]

ALLOWED_HOSTS = ['localhost']


SECRET_KEY = 'some-test-key'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
]

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
