import re
from typing import Annotated

from pydantic import AfterValidator
from util.strings import sanitize_html

from .common import StringOrNone

__all__ = [
    "SafeHtmlOrNone",
]


def _sanitize_html(html: str | None) -> str | None:
    if html is None:
        return None

    sanitized = sanitize_html(
        html,
        allow_tags={"p", "br", "a", "ul", "ol", "li"},
        allow_attrs={"a": {"href"}},
    )

    return sanitized


type SafeHtmlOrNone = Annotated[
    StringOrNone,
    AfterValidator(_sanitize_html),
]
