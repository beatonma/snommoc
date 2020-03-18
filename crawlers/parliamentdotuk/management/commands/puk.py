"""
Update data from parliament.uk with `python manage.py puk`
"""

import logging

from django.core.management import BaseCommand

from crawlers.parliamentdotuk.tasks import update_all_member_data

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-async',
            action='store_true',
            help='Pass update task to Celery.',
        )

    def handle(self, *args, **options):
        if options['async']:
            update_all_member_data.delay()
        else:
            update_all_member_data()
