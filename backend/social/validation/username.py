from util.settings import snommoc_settings


class BlockedUsername(Exception):
    def __init__(self, blocked_name):
        self.blocked_name = blocked_name

    def __str__(self):
        return f'BlockedUsername="{self.blocked_name}"'


def is_username_blocked(
    name: str,
    block_exact: list[str] | None = None,
    block_substring: list[str] | None = None,
) -> bool:
    if block_exact is None:
        block_exact = snommoc_settings.social.username_blocked_exact
    if block_substring is None:
        block_substring = snommoc_settings.social.username_blocked_substrings

    simple_name = "".join(c for c in name if c.isalpha()).lower()

    # Specific words that we want to reserve but may appear as a substring.
    for blocked in block_exact:
        if blocked == simple_name:
            return True

    # Strings that must not appear anywhere in the name.
    for blocked in block_substring:
        if blocked in simple_name:
            return True

    return False
