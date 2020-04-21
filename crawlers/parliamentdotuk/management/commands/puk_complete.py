"""

"""

import logging

from celery import shared_task
from django.core.management import BaseCommand

from crawlers.parliamentdotuk.tasks import update_constituencies
from crawlers.parliamentdotuk.tasks.membersdataplatform import update_all_members_basic_info
from crawlers.parliamentdotuk.tasks.membersdataplatform.active_members import update_all_member_details

log = logging.getLogger(__name__)


@shared_task
def complete_update():
    log.info('Updating constituencies...')
    update_constituencies()
    log.info('Updating all member basic info...')
    update_all_members_basic_info()
    log.info('Updating details for all members...')
    update_all_member_details()

    log.info('update_all_member_data completed.')


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        complete_update.delay()
