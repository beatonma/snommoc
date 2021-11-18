"""
Functions for updating information on all MPs, both current and historical.
This is the baseline - we will need to provide additional data for active MPs.
"""
from celery import shared_task

from crawlers.network import json_cache
from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints, mdp_client
from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import (
    MemberResponseData,
)
from notifications.models.task_notification import task_notification
from repository.models import Constituency, House, LordsType, Person
from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS
from repository.models.party import get_or_create_party
from repository.models.util.queryset import get_or_none
from repository.resolution.constituency import (
    get_constituency_for_date,
    get_current_constituency,
)
from repository.resolution.members import normalize_name

CACHE_NAME = "all-members"


@shared_task
@task_notification(label="Update all members basic info")
@json_cache(name=CACHE_NAME)
def update_all_members_basic_info(**kwargs):
    update_all_mps_basic_info(**kwargs)
    update_all_lords_basic_info(**kwargs)


@shared_task
@task_notification(label="Update all MPs basic info")
@json_cache(name=CACHE_NAME)
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
@json_cache(name=CACHE_NAME)
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
    house, _ = House.objects.get_or_create(name=data.get_house())

    if house.name == HOUSE_OF_COMMONS:
        _update_mp_basic_info(data, house)
    elif house.name == HOUSE_OF_LORDS:
        _update_lord_basic_info(data, house)


def _update_lord_basic_info(data: MemberResponseData, house: House) -> None:
    member_id = data.get_parliament_id()

    party = get_or_create_party(data.get_party_id(), data.get_party())
    is_active = data.get_is_active()

    try:
        lords_type, _ = LordsType.objects.get_or_create(name=data.get_lords_type())
    except:
        lords_type = None

    Person.objects.update_or_create(
        parliamentdotuk=member_id,
        defaults={
            "name": normalize_name(data.get_name()),
            "full_title": data.get_full_title(),
            "party": party,
            "lords_type": lords_type,
            "house": house,
            "date_entered_house": data.get_house_start_date(),
            "date_left_house": data.get_house_end_date(),
            "date_of_birth": data.get_date_of_birth(),
            "date_of_death": data.get_date_of_death(),
            "gender": data.get_gender(),
            "active": is_active,
        },
    )


def _update_mp_basic_info(data: MemberResponseData, house: House) -> None:
    member_id = data.get_parliament_id()

    party = get_or_create_party(data.get_party_id(), data.get_party())
    is_active = data.get_is_active()

    if is_active:
        constituency = get_current_constituency(data.get_constituency())
    else:
        constituency = get_constituency_for_date(
            data.get_constituency(),
            data.get_house_end_date() or data.get_house_start_date(),
        )

    person, _ = Person.objects.update_or_create(
        parliamentdotuk=member_id,
        defaults={
            "name": normalize_name(data.get_name()),
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
