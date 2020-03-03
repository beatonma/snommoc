"""
Update Divisions with:
    python manage.py divisions
"""

import logging

from django.core.management import BaseCommand

from crawlers.parliamentdotuk.tasks.lda.divisions import (
    update_commons_divisions,
    update_lords_divisions,
)
from repository.models import (
    LordsDivision,
    LordsDivisionVote,
    CommonsDivision,
    CommonsDivisionVote,
)

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-clear',
            action='store_true',
            help='Delete all divisions and related votes',
        )

    def handle(self, *args, **options):
        if options['clear']:
            for M in [
                LordsDivision,
                CommonsDivision,
                LordsDivisionVote,
                CommonsDivisionVote,
            ]:
                M.objects.all().delete()
        else:
            update_commons_divisions()
            update_lords_divisions()
