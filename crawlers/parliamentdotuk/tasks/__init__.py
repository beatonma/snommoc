from celery import shared_task

from notifications.models.task_notification import task_notification
from repository.models import UnlinkedConstituency
from .lda import (
    update_commons_divisions,
    update_constituencies,
    update_election_results,
)
from .membersdataplatform import (
    update_active_member_details,
    update_all_member_details,
    update_all_members_basic_info,
    update_member_portraits,
    update_member_portraits_wikipedia,
    update_missing_member_portraits_wikipedia,
)
from .openapi import update_lords_divisions


@shared_task
@task_notification(label="Update profiles for active members")
def update_profiles_for_active_members(**kwargs):
    _reset_unlinked_constituencies()

    update_constituencies()
    update_all_members_basic_info()
    update_active_member_details()


@shared_task
@task_notification(label="Update profiles for all members")
def update_profiles_for_all_members(**kwargs):
    _reset_unlinked_constituencies()

    update_constituencies()
    update_all_members_basic_info()
    update_all_member_details()


def _reset_unlinked_constituencies():
    """
    Clear any pre-existing UnlinkedConstituency instances. These are created while updating member data
    and are temporary placeholder objects. They should be consumed via staff dashboard actions after update completes.
    """
    UnlinkedConstituency.objects.all().delete()


@shared_task
@task_notification(label="Update Commons and Lords divisions")
def update_all_divisions(**kwargs):
    update_commons_divisions(**kwargs)
    update_lords_divisions(**kwargs)
