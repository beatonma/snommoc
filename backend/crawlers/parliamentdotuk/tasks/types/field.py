from typing import Any

from pydantic import AliasPath, Field
from pydantic_core import PydanticUndefined


def field(
    validation_alias: str,
    *,
    default: Any = PydanticUndefined,
    description: str | None = PydanticUndefined,
):
    """Convenience function for fields with validation_alias set.

    `validation_alias` may use dotted notation to indicate that the target
    data is nested in other objects - this will be resolved using AliasPath."""
    if "." in validation_alias:
        validation_alias = AliasPath(*validation_alias.split("."))

    default_factory = PydanticUndefined
    if callable(default):
        default_factory = default
        default = PydanticUndefined

    return Field(
        default=default,
        default_factory=default_factory,
        validation_alias=validation_alias,
        description=description,
    )
