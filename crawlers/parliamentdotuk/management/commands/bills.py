"""
Update Bills with:
    python manage.py bills
"""

import logging
from typing import Optional

from django.core.management import BaseCommand

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

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-clear',
            action='store_true',
            help='Delete all divisions and related votes',
        )
        parser.add_argument(
            '-async',
            action='store_true',
            help='Pass update_bills to Celery.',
        )
        parser.add_argument(
            '--id',
            type=int,
            help='Update a specific bill by parliamentdotuk ID',
        )
        parser.add_argument(
            '-fix',
            action='store_true',
            help='Try to fix bills that previously generated a BillUpdatedError',
        )

    def handle(self, *args, **options):
        if options['clear']:
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

        func_kwargs = {}
        if options['id']:
            func = update_bill
            func_kwargs = {
                'parliamentdotuk': options['id'],
            }
        else:
            func = update_bills

        if options['async']:
            func.delay(**func_kwargs)

        else:
            func(**func_kwargs)


def update_bill(parliamentdotuk: int) -> Optional[str]:
    log.info(f'Updating bill #{parliamentdotuk}')
    try:
        data = get_item_data(endpoints.BILL.format(parliamentdotuk=parliamentdotuk))
        log.info(data)
        if data is None:
            return None

        return _update_bill(parliamentdotuk, data)
    except Exception as e:
        BillUpdateError.create(parliamentdotuk, e)
        raise e


def fix_errored_bills():
    parliamentdotuk_ids = BillUpdateError.objects.values_list(
        'parliamentdotuk',
        flat=True
    )

    for parliamentdotuk in parliamentdotuk_ids:
        value = update_bill(parliamentdotuk)
        if value is not None:
            BillUpdateError.objects.filter(parliamentdotuk=parliamentdotuk).update(handled=True)
