"""

"""

import logging

from django.core.management import BaseCommand

from crawlers.parliamentdotuk.tasks.membersdataplatform.consolidation import consolidate_constituencies

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        consolidate_constituencies()

