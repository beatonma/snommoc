"""
Update Bills with:
    python manage.py bills
"""

import logging

from django.core.management import BaseCommand

from crawlers.parliamentdotuk.tasks.lda.bills import update_bills
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

        else:
            update_bills()
