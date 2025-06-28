from functools import partial

from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.divisions import schema
from crawlers.parliamentdotuk.tasks.openapi.divisions.shared import create_votes
from repository.models import CommonsDivision, House


@task_context(cache_name=caches.COMMONS_DIVISIONS)
def update_commons_divisions(context: TaskContext):
    openapi_client.foreach(
        endpoints.COMMONS_DIVISIONS_ALL,
        item_func=_get_single_commons_division,
        context=context,
    )


def _get_single_commons_division(response_data: dict, context: TaskContext):
    item = schema.CommonsDivisionItem.model_validate(response_data)
    house = House.objects.commons()

    openapi_client.get(
        endpoints.commons_division(item.division_id),
        item_func=partial(_update_commons_division, house),
        context=context,
    )


def _update_commons_division(house: House, response_data: dict, context: TaskContext):
    data = schema.CommonsDivision.model_validate(response_data)

    division, created = CommonsDivision.objects.update_or_create(
        parliamentdotuk=data.division_id,
        house=house,
        defaults={
            "title": data.title,
            "date": data.date,
            "number": data.number,
            "is_deferred_vote": data.is_deferred,
            "ayes": data.aye_count,
            "noes": data.no_count,
            "did_not_vote": len(data.did_not_vote),
            "is_passed": data.aye_count > data.no_count,
        },
    )

    create_votes(division, data.ayes, "aye")
    create_votes(division, data.noes, "no")
    create_votes(division, data.aye_tellers, "aye", is_teller=True)
    create_votes(division, data.no_tellers, "no", is_teller=True)
    create_votes(division, data.did_not_vote, "did_not_vote")

    if created:
        context.info(f"Created CommonsDivision '{division}'")
