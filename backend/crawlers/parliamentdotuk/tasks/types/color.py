import re
from typing import Annotated

from pydantic import AfterValidator

from .common import StringOrNone

__all__ = [
    "Color",
]


def _coerce_color(value: str | None) -> str | None:
    if value is None:
        return None
    if not value.startswith("#"):
        value = f"#{value}"
    if not re.match(r"#[0-9a-fA-F]{6}", value):
        return None
    return value.lower()


type Color = Annotated[StringOrNone, AfterValidator(_coerce_color)]
