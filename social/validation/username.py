"""

"""

import logging

from util.settings import get_social_settings

log = logging.getLogger(__name__)


class BlockedUsername(Exception):
    def __init__(self, blocked_name):
        self.blocked_name = blocked_name

    def __str__(self):
        return f'BlockedUsername="{self.blocked_name}"'


def is_username_blocked(name: str) -> bool:
    blocked_names = get_social_settings().get('USERNAME_BLOCKLIST', [])
    for blocked in blocked_names:
        if blocked in name:
            return True

    return False
