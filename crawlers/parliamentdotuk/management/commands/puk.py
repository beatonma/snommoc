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

        parser.add_argument(
            '-noconstituencies',
            action='store_false',
            dest='constituencies',
            default=True
        )

        parser.add_argument(
            '-nomemberbasic',
            action='store_false',
            dest='member_basic',
            default=True
        )

        parser.add_argument(
            '-nomemberdetail',
            action='store_false',
            dest='member_detail',
            default=True
        )

    def handle(self, *args, **options):
        kwargs = {
            'constituencies': options['constituencies'],
            'member_detail': options['member_detail'],
            'member_basic': options['member_basic'],
        }

        if options['async']:
            update_all_member_data.delay(**kwargs)
        else:
            update_all_member_data(**kwargs)
