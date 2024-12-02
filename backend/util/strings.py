from typing import Sequence

import nh3
from fuzzywuzzy import fuzz


def ellipsise(string: str, max_length: int = 32) -> str:
    """Trim the given string so that it is no more than max_length characters long."""
    if len(string) <= max_length:
        return string

    return f"{string[:max_length - 1]}…"


def sanitize_html(
    html: str,
    allow_tags: set[str] = None,
    allow_attrs: dict[str, set[str]] = None,
) -> str:
    return nh3.clean(
        html,
        tags=allow_tags or set(),
        attributes=allow_attrs or {},
        link_rel="noopener noreferrer nofollow",
    ).strip()


def get_similarity_score(a: Sequence, b: Sequence) -> int:
    return fuzz.token_sort_ratio(a, b)
