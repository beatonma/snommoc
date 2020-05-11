"""
See:
- https://data.parliament.uk/membersdataplatform/referencedata.aspx
- https://data.parliament.uk/membersdataplatform/memberquery.aspx
"""
import logging

from celery import shared_task

from .active_members import (
    update_active_member_details,
    update_all_member_details,
)
from .all_members import update_all_members_basic_info
from .member_portrait import update_member_portraits
from .. import update_constituencies
from ..lda.update_election_results import update_election_results

log = logging.getLogger(__name__)


@shared_task
def update_all_member_data(constituencies=True, member_basic=True, member_detail=True):
    if constituencies:
        log.info('Updating constituencies...')
        update_constituencies()
    if member_basic:
        log.info('Updating all member basic info...')
        update_all_members_basic_info()
    if member_detail:
        log.info('Updating active member details...')
        update_active_member_details()

    log.info('update_all_member_data completed.')


@shared_task
def complete_update():
    log.info('Updating constituencies...')
    update_constituencies()
    log.info('Updating all member basic info...')
    update_all_members_basic_info()
    log.info('Updating details for all members...')
    update_all_member_details()

    log.info('Updating election results')
    update_election_results()

    log.info('Updating member portraits...')
    update_member_portraits()

    log.info('complete_update completed.')
