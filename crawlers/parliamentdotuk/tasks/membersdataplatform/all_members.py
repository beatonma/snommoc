"""
Functions for updating information on all MPs, both current and historical.
This is the baseline - we will need to provide additional data for active MPs.
"""

import logging
from typing import (
    Tuple,
    Optional,
)

from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import MemberResponseData
from repository.models import (
    Constituency,
    Party,
    House,
)
from repository.models.houses import HOUSE_OF_COMMONS
from repository.models.person import Person
from . import (
    mdp_client,
    endpoints,
)

log = logging.getLogger(__name__)


def update_all_members_basic_info():
    update_all_mps_basic_info()
    update_all_lords_basic_info()


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
        endpoints.COMMONS_MEMBERS_ALL,
        _update_member_basic_info,
        _build_report
    )


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
        endpoints.LORDS_MEMBERS_ALL,
        _update_member_basic_info,
        _build_report
    )


def _update_member_basic_info(data: MemberResponseData) -> Optional[str]:
    parliamentdotuk = data.get_parliament_id()

    party, _ = Party.objects.get_or_create(name=data.get_party())
    constituency, _ = Constituency.objects.get_or_create(name=data.get_constituency())
    house, _ = House.objects.get_or_create(name=data.get_house())
    is_active = data.get_is_active()

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

    if is_active and house.name == HOUSE_OF_COMMONS:
        constituency.mp = person
        constituency.save()

    return person.name if created else None
