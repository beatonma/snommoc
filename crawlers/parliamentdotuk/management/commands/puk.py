"""
Update data from parliament.uk with `python manage.py puk`
"""

import logging

from django.core.management import BaseCommand

from crawlers.parliamentdotuk.tasks import (
    update_constituencies,
    update_all_member_data,
)
from repository.tasks import init_parties

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        init_parties()
        update_constituencies()
        update_all_member_data()
