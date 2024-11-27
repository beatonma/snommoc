import nh3


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
    ).strip()
