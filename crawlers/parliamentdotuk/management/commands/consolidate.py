"""

"""

import logging

from django.core.management import BaseCommand

from crawlers.parliamentdotuk.tasks.membersdataplatform.consolidation import consolidate_constituencies

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Try to merge partial constituencies retrieved from MDP with the canonical counterparts from LDA. Generates' \
           'ConstituencyAlsoKnownAs objects'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        consolidate_constituencies()
