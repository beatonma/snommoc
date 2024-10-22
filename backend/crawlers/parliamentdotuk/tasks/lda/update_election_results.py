import logging

from celery import shared_task
from crawlers import caches
from crawlers.context import TaskContext
from crawlers.network import JsonCache, json_cache
from crawlers.parliamentdotuk.tasks.lda import endpoints, lda_client
from crawlers.parliamentdotuk.tasks.lda import schema as lda_schema
from crawlers.parliamentdotuk.tasks.lda.lda_client import get_item_data
from notifications.models.task_notification import TaskNotification, task_notification
from repository.models import (
    Constituency,
    ConstituencyCandidate,
    ConstituencyResult,
    ConstituencyResultDetail,
    Election,
)
from repository.resolution.members import get_member_for_election_result, normalize_name
from repository.resolution.party import get_party_by_name

log = logging.getLogger(__name__)


def _create_election_result(
    parliamentdotuk: int, data: lda_schema.ElectionResultDetail
):
    constituency = Constituency.objects.get_or_none(
        parliamentdotuk=data.constituency.parliamentdotuk
    )
    election, _ = Election.objects.get_or_create(
        name=data.election.name,
        defaults={"parliamentdotuk": data.election.parliamentdotuk},
    )

    constituency_result, _ = ConstituencyResult.objects.get_or_create(
        election=election,
        constituency=constituency,
    )

    electorate = data.electorate
    turnout = data.turnout

    if not electorate or not turnout:
        turnout_fraction = 0
    else:
        turnout_fraction = turnout / electorate

    result, _ = ConstituencyResultDetail.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "constituency_result": constituency_result,
            "electorate": electorate,
            "majority": data.majority,
            "result": data.result_of_election,
            "turnout": turnout,
            "turnout_fraction": turnout_fraction,
        },
    )

    for candidate in data.candidates:
        _create_candidate(result, candidate, constituency, election)


def _create_candidate(
    election_result: ConstituencyResultDetail,
    candidate: lda_schema.ElectionCandidate,
    constituency: Constituency,
    election: Election,
):
    person = get_member_for_election_result(
        normalize_name(candidate.name),
        constituency,
        election,
    )
    party_name = candidate.party_name
    party = get_party_by_name(party_name)

    ConstituencyCandidate.objects.update_or_create(
        election_result=election_result,
        name=candidate.name,
        defaults={
            "person": person,
            "votes": candidate.number_of_votes,
            "order": candidate.order,
            "party_name": party_name,
            "party": party,
        },
    )


def fetch_and_create_election_result(
    parliamentdotuk: int,
    context: TaskContext,
) -> None:
    data = get_item_data(
        type=lda_schema.ElectionResultDetail,
        endpoint=endpoints.url_for_election_result(parliamentdotuk),
        context=context,
    )

    _create_election_result(parliamentdotuk, data)


@shared_task
@task_notification(label="Update constituency results")
@json_cache(caches.ELECTION_RESULTS)
def update_election_results(
    follow_pagination=True,
    cache: JsonCache | None = None,
    notification: TaskNotification | None = None,
    force_update: bool = False,
) -> None:
    context = TaskContext(notification=notification, cache=cache)

    def update_result_details(
        data: lda_schema.ElectionResult, _context: TaskContext
    ) -> None:
        if (
            not force_update
            and ConstituencyResultDetail.objects.filter(
                parliamentdotuk=data.parliamentdotuk
            ).exists()
        ):
            # We already have the data
            return

        fetch_and_create_election_result(data.parliamentdotuk, context)

    lda_client.foreach(
        endpoints.ELECTION_RESULTS,
        lda_schema.ElectionResult,
        item_func=update_result_details,
        context=context,
        follow_pagination=follow_pagination,
    )
