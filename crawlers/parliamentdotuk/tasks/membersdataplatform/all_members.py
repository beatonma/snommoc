"""
Functions for updating information on all MPs, both current and historical.
This is the baseline - we will need to provide additional data for active MPs.
"""

import logging

from celery import shared_task

from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import (
    MemberResponseData,
)
from repository.models.util.queryset import get_or_none
from notifications.models.task_notification import task_notification
from repository.models import House
from repository.models.constituency import (
    Constituency,
    get_current_constituency,
    get_constituency_for_date,
)
from repository.models.houses import HOUSE_OF_COMMONS
from repository.models.party import get_or_create_party
from repository.models.person import Person
from crawlers.parliamentdotuk.tasks.membersdataplatform import mdp_client, endpoints

log = logging.getLogger(__name__)


@shared_task
@task_notification(label="Update all members basic info")
def update_all_members_basic_info(**kwargs):
    update_all_mps_basic_info(**kwargs)
    update_all_lords_basic_info(**kwargs)


@shared_task
@task_notification(label="Update all MPs basic info")
def update_all_mps_basic_info(**kwargs):
    """
    Refresh basic data for all MPs, both active and historic.
    https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons%7Cmembership=all/
    """

    mdp_client.update_members(
        endpoint_url=endpoints.COMMONS_MEMBERS_ALL,
        update_member_func=_update_member_basic_info,
        response_class=MemberResponseData,
        **kwargs,
    )


@shared_task
@task_notification(label="Update all Lords basic info")
def update_all_lords_basic_info(**kwargs):
    """
    Refresh basic data for all MPs, both active and historic.
    https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons%7Cmembership=all/
    """

    mdp_client.update_members(
        endpoint_url=endpoints.LORDS_MEMBERS_ALL,
        update_member_func=_update_member_basic_info,
        response_class=MemberResponseData,
        **kwargs,
    )


def _update_member_basic_info(data: MemberResponseData) -> None:
    member_id = data.get_parliament_id()

    party = get_or_create_party(data.get_party_id(), data.get_party())
    house, _ = House.objects.get_or_create(name=data.get_house())
    is_active = data.get_is_active()

    if is_active:
        constituency = get_current_constituency(data.get_constituency())
    else:
        constituency = get_constituency_for_date(
            data.get_constituency(), data.get_house_start_date()
        )

    person, created = Person.objects.update_or_create(
        parliamentdotuk=member_id,
        defaults={
            "name": data.get_name(),
            "full_title": data.get_full_title(),
            "party": party,
            "constituency": constituency,
            "house": house,
            "date_entered_house": data.get_house_start_date(),
            "date_left_house": data.get_house_end_date(),
            "date_of_birth": data.get_date_of_birth(),
            "date_of_death": data.get_date_of_death(),
            "gender": data.get_gender(),
            "active": is_active,
        },
    )

    if is_active and constituency and house.name == HOUSE_OF_COMMONS:
        # If the member is registered to some other constituency,
        # remove that relation first before updating.
        existing = get_or_none(Constituency, mp__pk=member_id)
        if existing:
            existing.mp = None
            existing.save()

        constituency.mp = person
        constituency.save()
