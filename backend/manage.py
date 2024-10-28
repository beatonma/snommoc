#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snommoc.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    if "makemigrations" in sys.argv:
        # Disable environment settings which have side effects, allowing
        # `makemigrations` to be run without setting up a complete environment.
        os.environ.setdefault("CREATE_ENVIRONMENT_PATHS", "False")
        os.environ.setdefault("LOGGING_ENABLED", "False")
        os.environ.setdefault("DATABASE_ENGINE", "none")

    main()
