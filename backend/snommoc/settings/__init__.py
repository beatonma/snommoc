from datetime import timedelta
from urllib.parse import urljoin

from .apps import INSTALLED_APPS
from .auth import AUTH_PASSWORD_VALIDATORS
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
    DEBUG,
    DOMAIN_NAME,
    MEDIA_ROOT,
    SECRET_KEY,
    STATIC_ROOT,
    USER_AGENT,
)
from .logging import LOGGING
from .middleware import MIDDLEWARE
from .templates import TEMPLATES

WSGI_APPLICATION = "snommoc.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
ROOT_URLCONF = "snommoc.urls"
APPEND_SLASH = False

# URLs
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
ADMIN_URL = "admin/"
DASHBOARD_URL = "dashboard/"
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


# Internal settings
# API Crawler
SNOMMOC = {
    "CACHE": {
        "CRAWLER_CACHE_TTL": int(timedelta(days=365).total_seconds()),
        "CRAWLER_CACHE_ROOT": "/tmp/snommoc/crawler_cache/",
    }
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

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "api.pagination.DefaultResultsSetPagination",
    "PAGE_SIZE": 100,
}

NINJA_PAGINATION_PER_PAGE = 25
NINJA_PAGINATION_CLASS = "ninja.pagination.LimitOffsetPagination"


# Debug
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: environment.DEBUG and not environment.TEST,
}
