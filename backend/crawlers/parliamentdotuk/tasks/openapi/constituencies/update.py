from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from repository.models import (
    Constituency,
    ConstituencyBoundary,
    ConstituencyCandidate,
    ConstituencyResult,
    ConstituencyResultDetail,
    Election,
    Person,
)
from repository.resolution.members import get_member_for_election_result, normalize_name

from ..parties.update import update_party
from ..schema import ResponseItem
from . import schema


@task_context(cache_name=caches.CONSTITUENCIES)
def update_constituencies(context: TaskContext):
    openapi_client.foreach(
        endpoint_url=endpoints.CONSTITUENCIES,
        item_func=_update_constituency,
        context=context,
    )


@task_context(cache_name=caches.CONSTITUENCIES)
def update_constituency_boundaries(context: TaskContext):
    for constituency in Constituency.objects.filter(end__isnull=True):
        openapi_client.get(
            endpoint_url=endpoints.constituency_boundary(constituency.parliamentdotuk),
            item_func=_update_boundary,
            context=context,
            func_kwargs={"constituency": constituency.parliamentdotuk},
        )


@task_context(cache_name=caches.ELECTION_RESULTS)
def update_election_results(context: TaskContext):
    for constituency in Constituency.objects.filter(end__isnull=True):
        openapi_client.get(
            endpoint_url=endpoints.constituency_election_results(
                constituency.parliamentdotuk
            ),
            item_func=_update_election_result,
            context=context,
            func_kwargs={"constituency_id": constituency.parliamentdotuk},
        )


def _update_constituency(data: dict, context: TaskContext):
    data = ResponseItem[schema.ConstituencyItem].model_validate(data)

    try:
        member = Person.objects.get(parliamentdotuk=data.member_id)
    except Person.DoesNotExist:
        member = None

    constituency, _ = Constituency.objects.update_or_create(
        parliamentdotuk=data.parliamentdotuk,
        defaults={
            "name": data.name,
            "mp": member,
            "start": data.start_date,
            "end": data.end_date,
        },
    )


def _update_boundary(data: dict, context: TaskContext, func_kwargs: dict):
    data = schema.ConstituencyBoundary.model_validate(data)

    ConstituencyBoundary.objects.update_or_create(
        constituency_id=func_kwargs["constituency_id"],
        defaults={
            "geo_json": data.geo_json,
        },
    )


def _update_election_result(data: dict, context: TaskContext, func_kwargs: dict):
    data = ResponseItem[list[schema.ElectionResult]].model_validate(data)
    constituency = Constituency.objects.get(
        parliamentdotuk=func_kwargs["constituency_id"]
    )

    for item in data.value:
        election, _ = Election.objects.get_or_create(
            parliamentdotuk=item.election_id,
            defaults={
                "name": item.election_name,
                "date": item.election_date,
            },
        )

        openapi_client.get(
            endpoint_url=endpoints.constituency_election_results_detail(
                constituency.parliamentdotuk, election.parliamentdotuk
            ),
            item_func=_update_election_result_detail,
            context=context,
            func_kwargs={"constituency": constituency, "election": election},
        )


def _update_election_result_detail(data: dict, context: TaskContext, func_kwargs: dict):
    data = ResponseItem[schema.ElectionResult].model_validate(data).value
    constituency = func_kwargs["constituency"]
    election = func_kwargs["election"]

    result, _ = ConstituencyResult.objects.update_or_create(
        constituency=constituency,
        election=election,
    )

    detail, _ = ConstituencyResultDetail.objects.update_or_create(
        constituency_result=result,
        defaults={
            "result": data.result,
            "turnout": data.turnout,
            "majority": data.majority,
            "electorate": data.electorate,
        },
    )

    for candidate in data.candidates:
        _update_candidate(candidate, detail, constituency, election)


def _update_candidate(
    candidate: schema.ElectionCandidate,
    detail: ConstituencyResultDetail,
    constituency: Constituency,
    election: Election,
):
    person = get_member_for_election_result(
        normalize_name(candidate.name),
        constituency,
        election,
    )
    party = None
    party_name = None
    if party_data := candidate.party:
        party = update_party(party_data)
        party_name = party.name

    ConstituencyCandidate.objects.update_or_create(
        election_result=detail,
        name=candidate.name,
        defaults={
            "person": person,
            "party": party,
            "party_name": party_name,
            "order": candidate.rank_order,
            "votes": candidate.votes,
        },
    )
