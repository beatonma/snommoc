"""
Update member portrait urls
"""

import logging

from util.management.async_command import AsyncCommand
from crawlers.parliamentdotuk.tasks import update_member_portraits

log = logging.getLogger(__name__)


class Command(AsyncCommand):
    def handle(self, *args, **options):
        self.handle_async(update_member_portraits, *args, **options)
