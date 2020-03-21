"""
Update member portrait urls
"""

import logging

from django.core.management import BaseCommand

from crawlers.parliamentdotuk.tasks.membersdataplatform.member_portrait import update_member_portraits

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
            update_member_portraits.delay()
        else:
            update_member_portraits()
