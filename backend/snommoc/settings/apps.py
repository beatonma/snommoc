INSTALLED_DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_THIRD_PARTY_APPS = [
    "django_filters",
    "django_extensions",
    "phonenumber_field",
    "rest_framework",
]

INSTALLED_PROJECT_APPS = [
    "api",
    "repository",
    "crawlers.parliamentdotuk",
    "notifications",
    "dashboard",
    "social",
    "surface",
]
INSTALLED_APPS = INSTALLED_DJANGO_APPS + INSTALLED_THIRD_PARTY_APPS + INSTALLED_PROJECT_APPS
