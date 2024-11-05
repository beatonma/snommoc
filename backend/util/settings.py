from datetime import timedelta
from pathlib import Path
from typing import Annotated, Any, Callable, Type

from django.conf import settings as project_settings
from pydantic import BaseModel as Schema
from pydantic import BeforeValidator, Field, ValidationError
from pydantic_core import PydanticUndefined


def _field(
    alias: str,
    *,
    default: Any = PydanticUndefined,
    default_factory: Any = PydanticUndefined,
) -> Any:
    return Field(
        validation_alias=alias,
        default=default,
        default_factory=default_factory,
        validate_default=True,
    )


def _validate_path(path: Path | str) -> Path:
    if not path:
        raise ValidationError("Path cannot be empty")
    if isinstance(path, str):
        return Path(path)
    return path


type CoercedPath = Annotated[Path, BeforeValidator(_validate_path)]
type Seconds = int

_DEFAULT_CACHE_TTL = int(timedelta(days=4).total_seconds())


class SettingsSchema(Schema):
    pass


def _default_schema[T: Type[SettingsSchema]](schema: T) -> Callable[[], T]:
    """Return a factory for the given schema type using its default values."""
    return lambda: schema.model_validate({})


class AuthSettings(SettingsSchema):
    api_read_requires_auth: bool = _field("API_READ_REQUIRES_AUTH", default=True)


class CacheSettings(SettingsSchema):
    crawler_root: CoercedPath = _field("CRAWLER_CACHE_ROOT")
    crawler_ttl: Seconds = _field(
        "CRAWLER_CACHE_TTL",
        default=_DEFAULT_CACHE_TTL,
    )
    wiki_ttl: Seconds = _field("WIKI_CACHE_TTL", default=_DEFAULT_CACHE_TTL)


class SocialSettings(SettingsSchema):
    username_blocked_exact: list[str] = _field(
        "USERNAME_BLOCKED_EXACT",
        default_factory=list,
    )
    username_blocked_substrings: list[str] = _field(
        "USERNAME_BLOCKED_SUBSTRINGS",
        default_factory=list,
    )


class SnommocSettings(SettingsSchema):
    auth: AuthSettings = _field("AUTH", default_factory=_default_schema(AuthSettings))
    cache: CacheSettings = _field(
        "CACHE", default_factory=_default_schema(CacheSettings)
    )
    social: SocialSettings = _field(
        "SOCIAL", default_factory=_default_schema(SocialSettings)
    )


snommoc_settings: SnommocSettings = SnommocSettings.model_validate(
    getattr(project_settings, "SNOMMOC")
)
