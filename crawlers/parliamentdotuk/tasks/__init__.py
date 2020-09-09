from celery import shared_task

from .lda import (
    update_constituencies,
    update_bills,
    update_all_divisions,
    update_commons_divisions,
    update_lords_divisions,
    update_election_results,
)
from .membersdataplatform import (
    update_member_portraits,
    update_all_members_basic_info,
    update_active_member_details,
    update_all_member_details,
)


@shared_task
def update_profiles_for_active_members():
    update_constituencies()
    update_all_members_basic_info()
    update_active_member_details()


@shared_task
def update_profiles_for_all_members():
    update_constituencies()
    update_all_members_basic_info()
    update_all_member_details()
