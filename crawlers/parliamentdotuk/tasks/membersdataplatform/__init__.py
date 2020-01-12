"""
See:
- https://data.parliament.uk/membersdataplatform/referencedata.aspx
- https://data.parliament.uk/membersdataplatform/memberquery.aspx
"""
import logging

from .active_members import update_active_member_details
from .all_members import update_all_members_basic_info

log = logging.getLogger(__name__)


def update_all_member_data():
    update_all_members_basic_info()
    update_active_member_details()
