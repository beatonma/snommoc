from datetime import date

from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.parties.update import update_party
from crawlers.parliamentdotuk.tasks.openapi.schema import ResponseItem
from dateutil.utils import today
from repository.models import House, LordsDemographics, PartyDemographics
from repository.models.houses import HouseType

from . import schema


@task_context(cache_name=caches.DEMOGRAPHICS)
def update_demographics(context: TaskContext, for_date: date | None = None):
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


def _update_party_demographics(
    response_data: dict, context: TaskContext, func_kwargs: dict
):
    house_name = func_kwargs["house_name"]
    data = ResponseItem[schema.PartyDemographics].model_validate(response_data).value

    house, _ = House.objects.get_or_create(name=house_name)
    party = update_party(data.party, update=True)

    result, _ = PartyDemographics.objects.update_or_create(
        party=party,
        house=house,
        defaults={
            "male_member_count": data.male_member_count,
            "female_member_count": data.female_member_count,
            "non_binary_member_count": data.non_binary_member_count,
            "total_member_count": data.total_member_count,
        },
    )


def _update_lords_demographics(response_data: dict, context: TaskContext):
    data = ResponseItem[schema.LordsDemographics].model_validate(response_data).value

    party = update_party(data.party, update=True)

    result, _ = LordsDemographics.objects.update_or_create(
        party=party,
        defaults={
            "life_count": data.life_count,
            "hereditary_count": data.hereditary_count,
            "bishop_count": data.bishop_count,
            "total_count": data.total_count,
        },
    )
