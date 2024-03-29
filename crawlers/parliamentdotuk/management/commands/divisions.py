"""
Update Divisions with:
    python manage.py divisions
"""
from typing import Optional

from crawlers import caches
from crawlers.parliamentdotuk.tasks import (
    update_all_divisions,
    update_commons_divisions,
)
from crawlers.parliamentdotuk.tasks.lda.divisions import (
    fetch_and_create_commons_division,
)
from crawlers.parliamentdotuk.tasks.openapi.divisions.lords import (
    fetch_and_update_lords_division,
    update_lords_divisions,
)
from util.management.async_command import AsyncCommand

COMMONS = "commons"
LORDS = "lords"


class Command(AsyncCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "-commons",
            action="store_true",
            help="Only update Commons divisions.",
        )
        parser.add_argument(
            "-lords",
            action="store_true",
            help="Only update Lords divisions.",
        )
        parser.add_argument(
            "--id",
            type=int,
            help="Update a specific division. Use -lords or -commons to define the correct house (Commons assumed by default)",
            default=None,
        )

    def handle(self, *args, **command_options):
        id = command_options["id"]
        house = self._get_house(**command_options)

        if id is not None:
            func_kwargs = {
                "parliamentdotuk": id,
            }

            if house == LORDS:
                func_kwargs["cache"] = caches.LORDS_DIVISIONS
                func = fetch_and_update_lords_division
            else:
                func_kwargs["cache"] = caches.COMMONS_DIVISIONS
                func = fetch_and_create_commons_division

            func(**func_kwargs)

        else:
            if house == COMMONS:
                func = update_commons_divisions
            elif house == LORDS:
                func = update_lords_divisions
            else:
                func = update_all_divisions

            self.handle_async(func, **command_options)

    def _get_house(self, **command_options) -> Optional[str]:
        if command_options[COMMONS]:
            return COMMONS
        elif command_options[LORDS]:
            return LORDS
