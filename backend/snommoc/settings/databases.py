from . import environment
from .environment import DatabaseEngine


def _get_default_database(engine: DatabaseEngine):
    if engine == DatabaseEngine.SQLITE3:
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": environment.DATABASE_SQLITE_LOCATION
            / f"{environment.DATABASE_NAME}.sqlite3",
        }

    if engine == DatabaseEngine.POSTGRES:
        return {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": environment.DATABASE_NAME,
            "USER": environment.POSTGRES_USER,
            "PASSWORD": environment.POSTGRES_PASSWORD,
            "HOST": environment.POSTGRES_HOST,
            "PORT": environment.POSTGRES_PORT,
        }


def _get_databases(engine: DatabaseEngine):
    if engine == DatabaseEngine.NONE:
        return {}

    return {"default": _get_default_database(engine)}


DATABASES = _get_databases(environment.DATABASE_ENGINE)
