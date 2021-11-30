"""
Update Bills with:
    python manage.py bills
"""

import logging
from typing import Optional

from crawlers import caches
from crawlers.network import json_cache
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.bills import _update_bill, update_bills
from crawlers.parliamentdotuk.tasks.lda.lda_client import get_item_data
from repository.models import (
    Bill,
    BillPublication,
    BillSponsor,
    BillStage,
    BillStageSitting,
    BillStageType,
    BillType,
)
from util.management.async_command import AsyncCommand

log = logging.getLogger(__name__)


class Command(AsyncCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "-clear",
            action="store_true",
            help="Delete all divisions and related votes",
        )
        parser.add_argument(
            "--id",
            type=int,
            help="Update a specific bill by parliamentdotuk ID",
        )

    def handle(self, *args, **command_options):
        if command_options["clear"]:
            _clear_bill_data()

        if command_options["id"]:
            update_single_bill(command_options["id"])
            return
        else:
            func = update_bills

        self.handle_async(func, *args, **command_options)


def _clear_bill_data():
    for M in [
        BillPublication,
        BillSponsor,
        BillStageSitting,
        BillType,
        BillStageType,
        BillStage,
        Bill,
    ]:
        M.objects.all().delete()


@json_cache(caches.BILLS)
def update_single_bill(parliamentdotuk: int, **kwargs) -> Optional[str]:
    log.info(f"Updating bill #{parliamentdotuk}")
    try:
        data = get_item_data(endpoints.url_for_bill(parliamentdotuk), **kwargs)
        log.info(data)
        if data is None:
            print("No data")
            return

        return _update_bill(parliamentdotuk, data)
    except Exception as e:
        raise e
