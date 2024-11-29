from typing import Annotated

from pydantic import AfterValidator
from util.strings import sanitize_html

from .common import StringOrNone

__all__ = [
    "SafeHtmlOrNone",
]
type SafeHtmlOrNone = Annotated[
    StringOrNone,
    AfterValidator(
        lambda html: (
            sanitize_html(
                html,
                allow_tags={"p", "br", "a", "ul", "ol", "li"},
                allow_attrs={"a": {"href"}},
            )
            if html
            else None
        )
    ),
]
