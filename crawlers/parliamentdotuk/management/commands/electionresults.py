from util.management.async_command import AsyncCommand
from crawlers.parliamentdotuk.tasks.lda.update_election_results import (
    update_election_results,
)


class Command(AsyncCommand):
    def handle(self, *args, **options):
        self.handle_async(update_election_results, *args, **options)
