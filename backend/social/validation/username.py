from util.settings import get_social_settings
import util.settings_contract as contract


class BlockedUsername(Exception):
    def __init__(self, blocked_name):
        self.blocked_name = blocked_name

    def __str__(self):
        return f'BlockedUsername="{self.blocked_name}"'


def is_username_blocked(name: str) -> bool:
    settings = get_social_settings()
    simple_name = "".join(c for c in name if c.isalpha()).lower()

    # Specific words that we want to reserve but may appear as a substring.
    blocked_complete = settings.get(contract.SOCIAL_USERNAME_BLOCKED_EXACT, [])
    for blocked in blocked_complete:
        if blocked == simple_name:
            return True

    # Strings that must not appear anywhere in the name.
    blocked_substrings = settings.get(contract.SOCIAL_USERNAME_BLOCKED_SUBSTRINGS, [])
    for blocked in blocked_substrings:
        if blocked in simple_name:
            return True

    return False
