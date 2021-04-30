"""
Django settings for snommoc project.

Required attributes from local settings:
    BASE_DIR,
    VIRTUALENV_DIR,
    VIRTUALENV_ACTIVATE,
    DEBUG,
    SECRET_KEY,
    DOMAIN_NAME,
    ALLOWED_HOSTS,
    SNOMMOC_APPS,
    DATABASES,
    USER_AGENT,
    HTTP_REQUEST_HEADERS,
    REST_FRAMEWORK,

Optional attributes from local settings:
    SNOMMOC: {
        SOCIAL: {
            USERNAME_BLOCKLIST: List[str]  # List of disallowed usernames - e.g. reserved for use or abusive.
        }
    }
"""

import os
from .local_settings import *
from .installed_apps import INSTALLED_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "snommoc.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "snommoc.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = "/static/"
STATICFILES_DIRS = (
    os.path.join("rest_framework/static/"),
    os.path.join("dashboard/static/"),
)
MEDIA_URL = "/media/"
CRAWLER_CACHE_ROOT = os.path.join(BASE_DIR, "cache/")

APPEND_SLASH = False
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
