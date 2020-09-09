"""

"""

import logging

from social.tasks import update_recent_engagement
from util.management.async_command import AsyncCommand

log = logging.getLogger(__name__)


class Command(AsyncCommand):
    def handle(self, *args, **options):
        func = update_recent_engagement

        self.handle_async(func, *args, **options)
