"""
Update Bills with:
    python manage.py bills
"""

import logging
from typing import Optional

from crawlers.parliamentdotuk.models import BillUpdateError
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.bills import (
    update_bills,
    _update_bill,
)
from crawlers.parliamentdotuk.tasks.lda.lda_client import get_item_data
from repository.models import (
    Bill,
    BillSponsor,
    BillPublication,
    BillStage,
    BillStageSitting,
    BillStageType,
    BillType,
)
from crawlers.parliamentdotuk.tasks.network import json_cache
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
        parser.add_argument(
            "-fix",
            action="store_true",
            help="Try to fix bills that previously generated a BillUpdatedError",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            _clear_bill_data()

        func_kwargs = {}
        if options["id"]:
            options["instant"] = True
            func = _update_bill
            func_kwargs = {
                "parliamentdotuk": options["id"],
            }
        elif options["fix"]:
            options["instant"] = True
            func = _fix_errored_bills
        else:
            func = update_bills

        options.update(func_kwargs)

        self.handle_async(func, *args, **options)


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


@json_cache(name="bills")
def __update_bill(parliamentdotuk: int, **kwargs) -> Optional[str]:
    log.info(f"Updating bill #{parliamentdotuk}")
    try:
        data = get_item_data(endpoints.url_for_bill(parliamentdotuk), **kwargs)
        log.info(data)
        if data is None:
            return None

        return _update_bill(parliamentdotuk, data)
    except Exception as e:
        BillUpdateError.create(parliamentdotuk, e)
        raise e


def _fix_errored_bills():
    parliamentdotuk_ids = BillUpdateError.objects.values_list(
        "parliamentdotuk", flat=True
    )

    for parliamentdotuk in parliamentdotuk_ids:
        value = __update_bill(parliamentdotuk)
        if value is not None:
            BillUpdateError.objects.filter(parliamentdotuk=parliamentdotuk).update(
                handled=True
            )
