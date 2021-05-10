DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_filters",
    "django_extensions",
    "phonenumber_field",
    "rest_framework",
]

SNOMMOC_APPS = [
    "api",
    "repository",
    "crawlers.parliamentdotuk",
    "notifications",
    "dashboard",
    "social",
    "surface",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + SNOMMOC_APPS
