def ellipsise(string: str, max_length: int = 32) -> str:
    """Trim the given string so that it is no more than max_length characters long."""
    if len(string) <= max_length:
        return string

    return f"{string[:max_length - 1]}…"
