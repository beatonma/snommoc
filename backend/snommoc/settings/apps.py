from . import environment

INSTALLED_DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
]

INSTALLED_THIRD_PARTY_APPS = [
    "django_filters",
    "django_extensions",
    "phonenumber_field",
]

INSTALLED_PROJECT_APPS = [
    "api",
    "repository",
    "crawlers",
    "notifications",
    "dashboard",
    "social",
    "surface",
]
if environment.DEBUG and not environment.TEST:
    INSTALLED_THIRD_PARTY_APPS.append("debug_toolbar")


INSTALLED_APPS = (
    INSTALLED_DJANGO_APPS + INSTALLED_THIRD_PARTY_APPS + INSTALLED_PROJECT_APPS
)
