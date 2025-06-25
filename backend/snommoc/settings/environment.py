import logging
import os
import re
import sys
from enum import StrEnum
from pathlib import Path

log = logging.getLogger(__name__)


def _env_str(
    key: str,
    default: str | None = None,
    allow_blank: bool = False,
) -> str | None:
    value = os.environ.get(key, default)
    if value == "":
        if allow_blank:
            log.warning(f"Blank value for environment.{key}")
        else:
            value = default
    if value is None and default is not None:
        log.warning(f"Using default value for environment.{key}")
    return value


def _env_bool(key: str, default: bool) -> bool:
    return _env_str(key, str(default)).lower() == "true"


def _env_int(key: str, default: int | None = None) -> int | None:
    return int(_env_str(key, str(default)))


def _env_path(key: str, default: Path | str | None = None) -> Path | None:
    path_str = _env_str(key, None if default is None else str(default))
    if path_str is None:
        return None
    path = BASE_DIR / path_str
    if CREATE_ENVIRONMENT_PATHS and not path.exists():
        path.mkdir(mode=0o775, parents=False, exist_ok=True)
    return path


class DatabaseEngine(StrEnum):
    NONE = "none"
    POSTGRES = "postgres"
    SQLITE3 = "sqlite3"


DEBUG: bool = _env_bool("DEBUG", False)
TEST: bool = "test" in sys.argv

# Core
ADMIN_URL: str = _env_str("ADMIN_URL", "/dev-admin/")
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
SECRET_KEY: str = _env_str("SECRET_KEY")
DOMAIN_NAME: str = _env_str("DOMAIN_NAME")  # example.org
SITE_NAME: str = _env_str("SITE_NAME", DOMAIN_NAME or "untitled")
PROJECT_ID: str = re.sub(
    r"[^-\w]+]",
    "_",
    _env_str("PROJECT_ID", SITE_NAME),
)
USER_AGENT: str = _env_str("USER_AGENT")

# Database
DATABASE_ENGINE: DatabaseEngine = DatabaseEngine[
    _env_str("DATABASE_ENGINE", "sqlite3").upper()
]
DATABASE_NAME: str = _env_str("DATABASE_NAME", "database")
POSTGRES_USER: str = _env_str("POSTGRES_USER")
POSTGRES_PASSWORD: str = _env_str("POSTGRES_PASSWORD")
POSTGRES_HOST: str = _env_str("POSTGRES_HOST")
POSTGRES_PORT: int = _env_int("POSTGRES_PORT", 5432)

# Cache
CACHE_LOCATION: str = _env_str("CACHE_LOCATION")

# Email
SERVER_EMAIL: str = _env_str("SERVER_EMAIL")
EMAIL_HOST: str = _env_str("EMAIL_HOST")
EMAIL_PORT: int = _env_int("EMAIL_PORT", -1)
EMAIL_HOST_USER: str = _env_str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD: str = _env_str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS: bool = _env_bool("EMAIL_USE_TSL", True)
EMAIL_USE_SSL: bool = _env_bool("EMAIL_USE_SSL", False)

# File paths
CREATE_ENVIRONMENT_PATHS: bool = _env_bool("CREATE_ENVIRONMENT_PATHS", True)
DATABASE_SQLITE_LOCATION: Path = _env_path("DATABASE_SQLITE_LOCATION")
WEBPACK_OUTPUT_ROOT: Path = _env_path("WEBPACK_OUTPUT_ROOT")
LOGGING_ENABLED: bool = _env_bool("LOGGING_ENABLED", True)
DJANGO_LOGGING_DIR: Path = _env_path("DJANGO_LOGGING_DIR", f"/var/log/{PROJECT_ID}")
MEDIA_ROOT: Path = _env_path("MEDIA_ROOT", "/var/www/media")
STATIC_ROOT: Path = _env_path("STATIC_ROOT", "/var/www/static")

# OAuth
G_CLIENT_ID: str = _env_str("G_CLIENT_ID", "")
