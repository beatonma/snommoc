"""
Update Divisions with:
    python manage.py divisions
"""
from typing import Optional

from crawlers.network.cache import create_json_cache
from crawlers.parliamentdotuk.tasks.lda.divisions import (
    fetch_and_create_commons_division,
    fetch_and_create_lords_division,
)
from util.management.async_command import AsyncCommand
from crawlers.parliamentdotuk.tasks import (
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

COMMONS = "commons"
LORDS = "lords"


class Command(AsyncCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "-clear",
            action="store_true",
            help="Delete all divisions and related votes",
        )
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
        if command_options["clear"]:
            for M in [
                LordsDivision,
                CommonsDivision,
                LordsDivisionVote,
                CommonsDivisionVote,
            ]:
                M.objects.all().delete()

            return

        id = command_options["id"]
        house = self._get_house(**command_options)
        func_kwargs = dict()

        if id is not None:
            func_kwargs["parliamentdotuk"] = id
            func_kwargs["cache"] = create_json_cache("divisions")

            if house == LORDS:
                func = fetch_and_create_lords_division
            else:
                func = fetch_and_create_commons_division

        else:
            if house == COMMONS:
                func = update_commons_divisions
            elif house == LORDS:
                func = update_lords_divisions
            else:
                func = update_all_divisions

        self.handle_async(func, func_kwargs=func_kwargs, **command_options)

    def _get_house(self, **command_options) -> Optional[str]:
        if command_options[COMMONS]:
            return COMMONS
        elif command_options[LORDS]:
            return LORDS
