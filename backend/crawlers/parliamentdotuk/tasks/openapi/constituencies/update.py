from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.network.exceptions import HttpClientError
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from repository.models import (
    Constituency,
    ConstituencyBoundary,
    ConstituencyCandidate,
    ConstituencyResult,
    ConstituencyResultDetail,
    Election,
    Party,
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
    qs = Constituency.objects.all()
    if context.historic:
        qs = qs.historic()
    else:
        qs = qs.current()

    for constituency in qs:
        try:
            openapi_client.get(
                endpoint_url=endpoints.constituency_boundary(
                    constituency.parliamentdotuk
                ),
                item_func=_update_boundary,
                context=context,
                func_kwargs={"constituency_id": constituency.parliamentdotuk},
            )
        except HttpClientError as e:
            from api import status

            if e.status_code != status.HTTP_404_NOT_FOUND:
                raise e


@task_context(cache_name=caches.ELECTION_RESULTS)
def update_election_results(context: TaskContext):
    qs = Constituency.objects.all()
    if context.historic:
        qs = qs.historic()
    else:
        qs = qs.current()

    for constituency in qs:
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
        member = resolve_person(
            member_data.parliamentdotuk,
            member_data.name,
            party_schema=member_data.party,
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

    if geojson := data.geojson:
        ConstituencyBoundary.objects.update(
            geojson=geojson,
            constituency_id=func_kwargs["constituency_id"],
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

    winner_name, winner_person = _get_winning_candidate(
        constituency.name, data.candidates
    )

    result, _ = ConstituencyResult.objects.get_or_create(
        constituency=constituency,
        election=election,
        defaults={
            "winner": winner_person,
            "winner_name": winner_name,
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
    constituency_name: str,
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
            winner = x

    if not winner:
        return None, None

    person, party = _resolve_candidate_attributes(constituency_name, winner)

    if person:
        return None, person

    return winner.name, None


def _update_candidate(
    candidate: schema.ElectionCandidate,
    detail: ConstituencyResultDetail,
):
    person, party = _resolve_candidate_attributes(
        detail.constituency_result.constituency.name, candidate
    )

    ConstituencyCandidate.objects.update_or_create(
        election_result=detail,
        name=candidate.name,
        defaults={
            "person": person,
            "party": party,
            "order": candidate.rank_order,
            "result_change": candidate.result_change,
            "votes": candidate.votes,
        },
    )


def _resolve_candidate_attributes(
    constituency_name: str,
    candidate: schema.ElectionCandidate,
) -> tuple[Person | None, Party | None]:
    party = update_party(candidate.party) if candidate.party else None
    person = resolve_person(
        person_id=candidate.parliamentdotuk,
        name=candidate.name,
        party=party,
    )

    if not person:
        person = Person.objects.get_for_constituency(candidate.name, constituency_name)

    return person, party
