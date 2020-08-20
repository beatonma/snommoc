"""

"""

import logging

from util.management.async_command import AsyncCommand
from crawlers.parliamentdotuk.tasks.lda.update_election_results import update_election_results

log = logging.getLogger(__name__)


class Command(AsyncCommand):
    def handle(self, *args, **options):
        self.handle_async(update_election_results, *args, **options)
