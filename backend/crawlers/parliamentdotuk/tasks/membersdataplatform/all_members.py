"""
Functions for updating information on all MPs, both current and historical.
This is the baseline - we will need to provide additional data for active MPs.
"""

from celery import shared_task
from crawlers import caches
from crawlers.context import TaskContext
from crawlers.network import JsonCache, json_cache
from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints, mdp_client
from notifications.models import TaskNotification
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

from . import schema


@shared_task
@task_notification(label="Update all members basic info")
@json_cache(caches.MEMBERS)
def update_all_members_basic_info(
    notification: TaskNotification,
    cache: JsonCache | None = None,
):
    update_all_mps_basic_info(notification=notification, cache=cache)
    update_all_lords_basic_info(notification=notification, cache=cache)


@shared_task
@task_notification(label="Update all MPs basic info")
@json_cache(caches.MEMBERS)
def update_all_mps_basic_info(
    notification: TaskNotification,
    cache: JsonCache | None = None,
):
    """
    Refresh basic data for all MPs, both active and historic.
    https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons%7Cmembership=all/
    """
    context = TaskContext(cache, notification)

    mdp_client.foreach(
        url=endpoints.COMMONS_MEMBERS_ALL,
        item_func=_update_member_basic_info,
        context=context,
    )


@shared_task
@task_notification(label="Update all Lords basic info")
@json_cache(caches.MEMBERS)
def update_all_lords_basic_info(
    notification: TaskNotification,
    cache: JsonCache | None = None,
):
    """
    Refresh basic data for all MPs, both active and historic.
    https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons%7Cmembership=all/
    """

    context = TaskContext(cache, notification)

    mdp_client.foreach(
        url=endpoints.LORDS_MEMBERS_ALL,
        item_func=_update_member_basic_info,
        context=context,
    )


def _update_member_basic_info(data: schema.Member, context: TaskContext) -> None:
    house, _ = House.objects.get_or_create(name=data.house)

    if house.name == HOUSE_OF_COMMONS:
        _update_mp_basic_info(data, house)
    elif house.name == HOUSE_OF_LORDS:
        _update_lord_basic_info(data, house)


def _update_lord_basic_info(data: schema.Member, house: House) -> None:
    member_id = data.parliamentdotuk

    party = get_or_create_party(data.party.parliamentdotuk, data.party.name)

    try:
        lords_type, _ = LordsType.objects.get_or_create(name=data.lords_type)
    except:
        lords_type = None

    Person.objects.update_or_create(
        parliamentdotuk=member_id,
        defaults={
            "name": normalize_name(data.name),
            "full_title": data.full_title,
            "party": party,
            "lords_type": lords_type,
            "house": house,
            "date_entered_house": data.house_start_date,
            "date_left_house": data.house_end_date,
            "date_of_birth": data.date_of_birth,
            "date_of_death": data.date_of_death,
            "gender": data.gender,
            "active": data.is_active,
        },
    )


def _update_mp_basic_info(data: schema.Member, house: House) -> None:
    member_id = data.parliamentdotuk

    party = get_or_create_party(data.party.parliamentdotuk, data.party.name)
    is_active = data.is_active

    if is_active:
        constituency = get_current_constituency(data.constituency_name)
    else:
        constituency = get_constituency_for_date(
            data.constituency_name,
            data.house_end_date or data.house_start_date,
        )

    person, _ = Person.objects.update_or_create(
        parliamentdotuk=member_id,
        defaults={
            "name": normalize_name(data.name),
            "full_title": data.full_title,
            "party": party,
            "constituency": constituency,
            "house": house,
            "date_entered_house": data.house_start_date,
            "date_left_house": data.house_end_date,
            "date_of_birth": data.date_of_birth,
            "date_of_death": data.date_of_death,
            "gender": data.gender,
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
