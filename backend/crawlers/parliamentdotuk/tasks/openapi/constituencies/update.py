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

from ..common import resolve_person
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
            func_kwargs={"constituency_id": constituency.parliamentdotuk},
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


def _update_constituency(response_data: dict, context: TaskContext):
    data = ResponseItem[schema.Constituency].model_validate(response_data).value
    member = None
    if member_data := data.member:
        party = member_data.party

        member = resolve_person(
            member_data.parliamentdotuk,
            member_data.name,
            party_schema=party,
        )

    constituency, _ = Constituency.objects.update_or_create(
        parliamentdotuk=data.parliamentdotuk,
        defaults={
            "name": data.name,
            "mp": member,
            "start": data.start_date,
            "end": data.end_date,
        },
    )


def _update_boundary(response_data: dict, context: TaskContext, func_kwargs: dict):
    data = schema.ConstituencyBoundary.model_validate(response_data)

    ConstituencyBoundary.objects.update_or_create(
        constituency_id=func_kwargs["constituency_id"],
        defaults={
            "geo_json": data.geo_json,
        },
    )


def _update_election_result(
    response_data: dict, context: TaskContext, func_kwargs: dict
):
    data = ResponseItem[list[schema.ElectionResult]].model_validate(response_data)
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


def _update_election_result_detail(
    response_data: dict, context: TaskContext, func_kwargs: dict
):
    data = ResponseItem[schema.ElectionResult].model_validate(response_data).value
    constituency = func_kwargs["constituency"]
    election = func_kwargs["election"]

    winner_name, winner_person = _get_winning_candidate(data.candidates)

    result, _ = ConstituencyResult.objects.get_or_create(
        constituency=constituency,
        election=election,
        defaults={
            "mp": winner_person,
            "mp_name": winner_name,
        },
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
        _update_candidate(candidate, detail)


def _get_winning_candidate(
    candidates: list[schema.ElectionCandidate],
) -> tuple[str | None, Person | None]:
    """Resolve a Person instance for the winner, or their name if resolution unsuccessful.

    Returns:
        (`None`, `None`) if the winning candidate could not be found at all - shouldn't happen.
        (`None`, `Person`) if a Person instance was resolved.
        (`str`, `None`) with the winner's name if a Person instance was not resolved.
    """
    winner: schema.ElectionCandidate | None = None
    for x in candidates:
        if x.rank_order == 1:
            winner = winner

    if not winner:
        return None, None

    if winner.parliamentdotuk:
        return None, resolve_person(
            winner.parliamentdotuk, name=winner.name, party_schema=winner.party
        )

    # Try to resolve Person instance by name
    winner_name = winner.name
    qs = Person.objects.filter_name(winner_name)
    if qs.count() == 1:
        return None, qs.first()

    return winner_name, None


def _update_candidate(
    candidate: schema.ElectionCandidate,
    detail: ConstituencyResultDetail,
):
    person = None
    if person_id := candidate.parliamentdotuk:
        person = Person.objects.get_or_none(parliamentdotuk=person_id)
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
