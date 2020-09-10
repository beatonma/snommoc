"""

"""

import logging

from surface.tasks import update_zeitgeist
from util.management.async_command import AsyncCommand

log = logging.getLogger(__name__)


class Command(AsyncCommand):
    def handle(self, *args, **options):
        func = update_zeitgeist

        self.handle_async(func, *args, **options)
