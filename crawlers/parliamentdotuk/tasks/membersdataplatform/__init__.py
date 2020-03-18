"""
See:
- https://data.parliament.uk/membersdataplatform/referencedata.aspx
- https://data.parliament.uk/membersdataplatform/memberquery.aspx
"""
import logging

from celery import shared_task

from .active_members import update_active_member_details
from .all_members import update_all_members_basic_info
from .. import update_constituencies

log = logging.getLogger(__name__)


@shared_task
def update_all_member_data():
    update_constituencies()
    update_all_members_basic_info()
    update_active_member_details()
