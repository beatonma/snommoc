"""
Update Divisions with:
    python manage.py divisions
"""

import logging

from crawlers.parliamentdotuk.management.commands.async_command import AsyncCommand
from crawlers.parliamentdotuk.tasks.lda.divisions import (
    update_commons_divisions,
    update_lords_divisions,
    update_all_divisions,
)
from repository.models import (
    LordsDivision,
    LordsDivisionVote,
    CommonsDivision,
    CommonsDivisionVote,
)

log = logging.getLogger(__name__)


class Command(AsyncCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            '-clear',
            action='store_true',
            help='Delete all divisions and related votes',
        )
        parser.add_argument(
            '-commons',
            action='store_true',
            help='Only update Commons divisions.',
        )
        parser.add_argument(
            '-lords',
            action='store_true',
            help='Only update Lords divisions.',
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

            return

        if options['commons']:
            func = update_commons_divisions
        elif options['lords']:
            func = update_lords_divisions
        else:
            func = update_all_divisions

        self.handle_async(func, *args, **options)
