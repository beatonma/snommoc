from datetime import timedelta
from urllib.parse import urljoin

from .apps import INSTALLED_APPS
from .auth import AUTH_PASSWORD_VALIDATORS
from .caching import CACHES
from .databases import DATABASES
from .email import (
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
    EMAIL_PORT,
    EMAIL_USE_SSL,
    EMAIL_USE_TLS,
    SERVER_EMAIL,
)
from .environment import (
    ADMIN_URL,
    DEBUG,
    DOMAIN_NAME,
    G_CLIENT_ID,
    MEDIA_ROOT,
    SECRET_KEY,
    STATIC_ROOT,
    USER_AGENT,
)
from .logging import LOGGING
from .middleware import MIDDLEWARE
from .templates import TEMPLATES

TEST_RUNNER = "basetest.runner.PytestTestRunner"

WSGI_APPLICATION = "snommoc.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
ROOT_URLCONF = "snommoc.urls"
APPEND_SLASH = False

# URLs
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
LOGIN_URL = urljoin(ADMIN_URL, "login/")

ALLOWED_HOSTS = ["localhost", "django", environment.DOMAIN_NAME]
CSRF_TRUSTED_ORIGINS = [
    f"https://{environment.DOMAIN_NAME}",
]
if DEBUG:
    CSRF_TRUSTED_ORIGINS += ["http://localhost:8000"]


# Internationalization
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# PhoneNumberField region
PHONENUMBER_DEFAULT_REGION = "GB"


# Internal settings
# API Crawler
SNOMMOC = {
    "CACHE": {
        "CRAWLER_CACHE_TTL": int(timedelta(days=365).total_seconds()),
        "CRAWLER_CACHE_ROOT": "/tmp/snommoc/crawler_cache/",
    },
    "AUTH": {
        "API_READ_REQUIRES_AUTH": False,
    },
}

# User agent attached to requests made to 3rd party API services
HTTP_REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
}
HTTP_REQUEST_HEADERS_JSON = {
    **HTTP_REQUEST_HEADERS,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

NINJA_PAGINATION_PER_PAGE = 24
NINJA_PAGINATION_CLASS = "api.pagination.LimitOffsetPagination"

# Debug
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: environment.DEBUG and not environment.TEST,
}
