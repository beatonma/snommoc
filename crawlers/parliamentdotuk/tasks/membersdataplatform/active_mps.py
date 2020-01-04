"""

"""

import logging
import time
from typing import (
    Optional,
    List,
)

from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints
from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import (
    update_members,
    MemberBiographyResponseData,
    ConstituencyResponseData,
    HouseMembershipResponseData,
    BasicInfoResponseData,
)
from repository.models import (
    ConstituencyResult,
    Constituency,
    Election,
    Country,
)
from repository.models.geography import Town
from repository.models.houses import (
    HOUSE_OF_COMMONS,
    House,
    HOUSE_OF_LORDS,
    HouseMembership,
)
from repository.models.person import Person

log = logging.getLogger(__name__)


def update_active_mps_details():
    active_mp_parliamentdotuk_ids = [
        person.parliamentdotuk for person
        in Person.objects.filter(
            active=True,
            house__name=HOUSE_OF_COMMONS,
        )
    ]

    for parliamentdotuk_id in active_mp_parliamentdotuk_ids:
        update_members(
            endpoints.member_biography(parliamentdotuk_id),
            update_member_func=update_member_biography,
            report_func=None,
            response_class=MemberBiographyResponseData,
        )
        time.sleep(1)


def update_member_biography(data: MemberBiographyResponseData) -> Optional[str]:
    parliamentdotuk: int = data.get_parliament_id()

    person = Person.objects.get(parliamentdotuk=parliamentdotuk)

    _update_basic_details(person, data.get_basic_info())
    _update_house_membership(person, data.get_house_memberships())
    _update_historical_constituencies(person, data.get_constituencies())


def _update_basic_details(person: Person, data: BasicInfoResponseData):
    person.given_name = data.get_first_name()
    person.additional_name = data.get_middle_names()
    person.family_name = data.get_family_name()

    town_name = data.get_town_of_birth()
    country_name = data.get_country_of_birth()
    if country_name:
        person.country_of_birth, _ = Country.objects.get_or_create(name=country_name)

        if town_name:
            person.town_of_birth, _ = Town.objects.get_or_create(
                name=town_name,
                country=person.country_of_birth,
            )

    person.save()


def _update_house_membership(
        person: Person,
        memberships: List[HouseMembershipResponseData]
):
    for hm in memberships:
        house, _ = House.objects.get_or_create(name=hm.get_house())
        HouseMembership.objects.update_or_create(
            person=person,
            house=house,
            start=hm.get_start_date(),
            defaults={
                'end': hm.get_end_date()
            }
        )


def _update_historical_constituencies(
        person: Person,
        historical_constituencies: List[ConstituencyResponseData]
):
    for c in historical_constituencies:
        constituency, _ = Constituency.objects.get_or_create(
            parliamentdotuk=c.get_constituency_id(),
            defaults={
                'name': c.get_constituency_name()
            }
        )
        election, _ = Election.objects.update_or_create(
            parliamentdotuk=c.get_election_id(),
            defaults={
                'name': c.get_election_name(),
                'date': c.get_election_date(),
            })

        result, _ = ConstituencyResult.objects.update_or_create(
            constituency=constituency,
            election=election,
            defaults={
                'start': c.get_start_date(),
                'end': c.get_end_date(),
                'mp': person,
            }
        )
