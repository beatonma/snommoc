"""
Update member portrait urls
"""
from crawlers.parliamentdotuk.tasks import (
    update_member_portraits,
    update_missing_member_portraits_wikipedia,
)
from util.management.async_command import AsyncCommand


class Command(AsyncCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "-wiki",
            action="store_true",
            default=False,
            help="Use confirmed wikipedia pages to find missing portraits.",
        )

    def handle(self, *args, **options):
        if options.get("wiki"):
            func = update_missing_member_portraits_wikipedia
        else:
            func = update_member_portraits

        self.handle_async(func, *args, **options)
