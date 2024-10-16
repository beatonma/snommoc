import logging
import os

from . import environment
from .apps import INSTALLED_DJANGO_APPS, INSTALLED_PROJECT_APPS


def _logger(level: str):
    return {
        "handlers": [
            "console",
            "file",
            "mail_admins",
        ],
        "level": level,
        "propagate": False,
    }


if not environment.LOGGING_ENABLED:
    LOGGING = None
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            }
        },
        "handlers": {
            "console": {
                "class": "rich.logging.RichHandler",
                "level": logging.DEBUG if environment.DEBUG else logging.INFO,
                "rich_tracebacks": True,
                "markup": True,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": logging.INFO,
                "filename": os.path.join(
                    environment.DJANGO_LOGGING_DIR,
                    f"{environment.PROJECT_ID}.log",
                ),
                "maxBytes": 1 * 1024 * 1024,
                "backupCount": 2,
            },
            "mail_admins": {
                "level": logging.ERROR,
                "class": "django.utils.log.AdminEmailHandler",
                "filters": ["require_debug_false"],
            },
        },
        "loggers": {
            **{app: _logger(logging.WARNING) for app in INSTALLED_DJANGO_APPS},
            **{app: _logger(logging.INFO) for app in INSTALLED_PROJECT_APPS},
        },
    }
