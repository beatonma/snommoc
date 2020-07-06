"""
Functions for updating information on all MPs, both current and historical.
This is the baseline - we will need to provide additional data for active MPs.
"""

import logging
from typing import (
    Tuple,
    Optional,
    Type,
)

from celery import shared_task
from django.db import models

from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import MemberResponseData
from repository.models import (
    House,
)
from repository.models.constituency import (
    get_current_constituency,
    get_constituency_for_date,
)
from repository.models.houses import HOUSE_OF_COMMONS
from repository.models.party import get_or_create_party
from repository.models.person import Person
from . import (
    mdp_client,
    endpoints,
)

log = logging.getLogger(__name__)


@shared_task
def update_all_members_basic_info():
    update_all_mps_basic_info()
    update_all_lords_basic_info()


@shared_task
def update_all_mps_basic_info():
    """
    Refresh basic data for all MPs, both active and historic.
    https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons%7Cmembership=all/
    """
    def _build_report(new_mps) -> Tuple[str, str]:
        title = 'Basic info updated for all MPs'
        if new_mps:
            name_list = '\n'.join(new_mps)
            content = f'{len(new_mps)} new MPs:\n{name_list}'
        else:
            content = 'No new MPs'
        return title, content

    mdp_client.update_members(
        endpoint_url=endpoints.COMMONS_MEMBERS_ALL,
        update_member_func=_update_member_basic_info,
        report_func=_build_report,
        response_class=MemberResponseData
    )


@shared_task
def update_all_lords_basic_info():
    """
    Refresh basic data for all MPs, both active and historic.
    https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons%7Cmembership=all/
    """
    def _build_report(new_lords) -> Tuple[str, str]:
        title = 'Basic info updated for all Lords'
        if new_lords:
            name_list = '\n'.join(new_lords)
            content = f'{len(new_lords)} new Lords:\n{name_list}'
        else:
            content = 'No new Lords'
        return title, content

    mdp_client.update_members(
        endpoint_url=endpoints.LORDS_MEMBERS_ALL,
        update_member_func=_update_member_basic_info,
        report_func=_build_report,
        response_class=MemberResponseData
    )


def _get_or_create_or_none(model_class: Type[models.Model], **kwargs) -> Tuple[Optional[models.Model], bool]:
    try:
        return model_class.objects.get_or_create(**kwargs)
    except Exception:
        return None, False


def _update_member_basic_info(data: MemberResponseData) -> Optional[str]:
    parliamentdotuk = data.get_parliament_id()

    party = get_or_create_party(data.get_party_id(), data.get_party())
    house, _ = _get_or_create_or_none(House, name=data.get_house())
    is_active = data.get_is_active()
    if is_active:
        constituency = get_current_constituency(data.get_constituency())
    else:
        constituency = get_constituency_for_date(data.get_constituency(), data.get_house_start_date())

    person, created = Person.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            'name': data.get_name(),
            'full_title': data.get_full_title(),
            'party': party,
            'constituency': constituency,
            'house': house,
            'date_entered_house': data.get_house_start_date(),
            'date_left_house': data.get_house_end_date(),
            'date_of_birth': data.get_date_of_birth(),
            'date_of_death': data.get_date_of_death(),
            'gender': data.get_gender(),
            'active': is_active,
        })

    if is_active and constituency and house.name == HOUSE_OF_COMMONS:
        constituency.mp = person
        constituency.save()

    return person.name if created else None
