import logging

from crawlers.parliamentdotuk.tasks.openapi.bills import (
    fetch_and_update_bill,
    update_bill_stage_types,
    update_bill_types,
    update_bills,
)
from util.management.async_command import AsyncCommand

log = logging.getLogger(__name__)


class Command(AsyncCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--id",
            type=int,
            help="Update a specific bill by parliamentdotuk ID",
        )

    def handle(self, *args, **command_options):
        if command_options["id"]:
            update_single_bill(command_options["id"])
            return
        else:
            func = update_bills

        self.handle_async(func, *args, **command_options)


def update_single_bill(parliamentdotuk: int, **kwargs):
    log.info(f"Updating bill #{parliamentdotuk}")

    update_bill_types()
    update_bill_stage_types()
    fetch_and_update_bill(parliamentdotuk)
