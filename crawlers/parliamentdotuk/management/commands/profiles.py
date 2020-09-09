"""

"""

import logging

from crawlers.parliamentdotuk.tasks import (
    update_profiles_for_active_members,
    update_profiles_for_all_members,
)
from util.management.async_command import AsyncCommand

log = logging.getLogger(__name__)


class Command(AsyncCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            '-all',
            action='store_true',
            default=False,
            help='Update profile details for active and historic members.'
        )

    def handle(self, *args, **kwargs):
        if kwargs['all']:
            func = update_profiles_for_all_members
        else:
            func = update_profiles_for_active_members

        self.handle_async(func, *args, **kwargs)
