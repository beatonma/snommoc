from datetime import date

from dateutil.utils import today

from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.parties.update import update_party
from crawlers.parliamentdotuk.tasks.openapi.schema import ResponseItem
from repository.models import (
    House,
    Party,
    PartyGenderDemographics,
    PartyLordsDemographics,
)
from repository.models.houses import HouseType

from . import schema


@task_context(cache_name=caches.DEMOGRAPHICS)
def update_demographics(context: TaskContext, for_date: date | None = None):
    PartyGenderDemographics.objects.all().delete()
    PartyLordsDemographics.objects.all().delete()

    houses: list[HouseType] = ["Commons", "Lords"]
    for_date: date = for_date or today()
    for house in houses:
        openapi_client.foreach(
            endpoints.party_states(house, for_date),
            item_func=_update_party_demographics,
            context=context,
            func_kwargs={"house_name": house},
        )

    openapi_client.foreach(
        endpoints.lords_states(for_date),
        item_func=_update_lords_demographics,
        context=context,
    )

    update_demographics_from_local_data(context=context)


def _update_party_demographics(
    response_data: dict, context: TaskContext, func_kwargs: dict
):
    house_name = func_kwargs["house_name"]
    data = (
        ResponseItem[schema.PartyGenderDemographics].model_validate(response_data).value
    )

    house, _ = House.objects.get_or_create(name=house_name)
    party = update_party(data.party, update=True)

    result, _ = PartyGenderDemographics.objects.update_or_create(
        party=party,
        house=house,
        defaults={
            "female_member_count": data.female_member_count,
            "male_member_count": data.male_member_count,
            "non_binary_member_count": data.non_binary_member_count,
            "total_member_count": data.total_member_count,
        },
    )


def _update_lords_demographics(response_data: dict, context: TaskContext):
    data = (
        ResponseItem[schema.PartyLordsDemographics].model_validate(response_data).value
    )

    party = update_party(data.party, update=True)

    result, _ = PartyLordsDemographics.objects.update_or_create(
        party=party,
        defaults={
            "life_count": data.life_count,
            "hereditary_count": data.hereditary_count,
            "bishop_count": data.bishop_count,
            "total_count": data.total_count,
        },
    )


def update_demographics_from_local_data(context: TaskContext = None):
    """Use local data to update demographics for parties that are not listed in Parliament API data.

    e.g. Labour (Co-op) data is aggregated with the main Labour party in Parliament data.
    """
    parties = Party.objects.filter(gender_demographics__isnull=True).prefetch_related(
        "person_set"
    )
    houses = (House.objects.commons(), House.objects.lords())

    for party in parties:
        all_members = party.person_set.current()

        for house in houses:
            house_members = all_members.filter(house=house)
            house_members_count = house_members.count()
            male_member_count = house_members.filter(gender="M").count()
            female_member_count = house_members.filter(gender="F").count()

            # As of 2025-07-25, no members are registered as non-binary in available Parliament API data.
            # This should be updated when that changes, but until then we don't know for certain what code
            # will be used to reference them and we will refrain from guessing.
            non_binary_member_count = 0

            PartyGenderDemographics.objects.update_or_create(
                party=party,
                house=house,
                defaults={
                    "female_member_count": female_member_count,
                    "male_member_count": male_member_count,
                    "non_binary_member_count": non_binary_member_count,
                    "total_member_count": house_members_count,
                },
            )
