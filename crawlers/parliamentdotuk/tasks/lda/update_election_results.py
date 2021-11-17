import logging

from celery import shared_task

from crawlers.network import JsonResponseCache, json_cache
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import electionresults as contract
from crawlers.parliamentdotuk.tasks.lda.lazy_update import lazy_update
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_int,
    get_item_data,
    get_list,
    get_parliamentdotuk_id,
    get_str,
    update_model,
)
from crawlers.parliamentdotuk.tasks.util.checks import check_required_fields
from notifications.models.task_notification import task_notification
from repository.models import (
    Constituency,
    ConstituencyCandidate,
    ConstituencyResult,
    ConstituencyResultDetail,
    Election,
)
from repository.models.util.queryset import get_or_none
from repository.resolution.members import get_member_for_election_result
from repository.resolution.party import get_party_by_name

log = logging.getLogger(__name__)


def _create_election_result(parliamentdotuk, data):
    check_required_fields(
        data,
        contract.CONSTITUENCY,
        contract.ELECTION,
        contract.RESULT_OF_ELECTION,
        contract.MAJORITY,
    )

    log.info(f"Updating constituency result {parliamentdotuk}...")

    constituency_id = get_parliamentdotuk_id(data, contract.CONSTITUENCY_ABOUT)
    election_name = get_str(data, contract.ELECTION_NAME)

    constituency = get_or_none(Constituency, parliamentdotuk=constituency_id)
    election, _ = Election.objects.get_or_create(
        name=election_name,
        defaults={
            "parliamentdotuk": get_parliamentdotuk_id(data, contract.ELECTION_ABOUT)
        },
    )

    constituency_result, _ = ConstituencyResult.objects.get_or_create(
        election=election,
        constituency=constituency,
    )

    electorate = get_int(data, contract.ELECTORATE)
    turnout = get_int(data, contract.TURNOUT)

    if not electorate or not turnout:
        turnout_fraction = 0
    else:
        turnout_fraction = turnout / electorate

    result, _ = ConstituencyResultDetail.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "constituency_result": constituency_result,
            "electorate": electorate,
            "majority": get_int(data, contract.MAJORITY),
            "result": get_str(data, contract.RESULT_OF_ELECTION),
            "turnout": turnout,
            "turnout_fraction": turnout_fraction,
        },
    )

    candidates = get_list(data, contract.CANDIDATES)
    for candidate in candidates:
        _create_candidate(result, candidate, constituency, election)


def _parse_candidate_name(raw_name: str) -> str:
    """Remove extraneous whitespace and re-order name if in Surname, Forename format"""
    normalised_whitespace = " ".join([x for x in raw_name.split(" ") if x])

    if "," in normalised_whitespace:
        parts = [x.strip() for x in normalised_whitespace.split(",")]
        return f"{' '.join(parts[1:])} {parts[0]}"
    else:
        return normalised_whitespace


def _create_candidate(
    election_result: ConstituencyResultDetail,
    candidate,
    constituency: Constituency,
    election: Election,
):
    check_required_fields(
        candidate,
        contract.CANDIDATE_NAME,
        contract.CANDIDATE_PARTY,
    )

    name = _parse_candidate_name(get_str(candidate, contract.CANDIDATE_NAME))
    person = get_member_for_election_result(name, constituency, election)
    party_name = get_str(candidate, contract.CANDIDATE_PARTY)
    party = get_party_by_name(party_name)

    votes = get_int(candidate, contract.CANDIDATE_VOTES)
    order = get_int(candidate, contract.CANDIDATE_ORDINAL)

    ConstituencyCandidate.objects.update_or_create(
        election_result=election_result,
        name=name,
        defaults={
            "person": person,
            "votes": votes,
            "order": order,
            "party_name": party_name,
            "party": party,
        },
    )


def fetch_and_create_election_result(
    parliamentdotuk: int,
    cache: JsonResponseCache,
) -> None:
    url = endpoints.url_for_election_result(parliamentdotuk)
    data = get_item_data(
        url,
        cache=cache,
    )

    _create_election_result(parliamentdotuk, data)


@shared_task
@task_notification(label="Update constituency results")
@json_cache(name="election-results")
def update_election_results(follow_pagination=True, **kwargs) -> None:
    def update_result_details(json_data) -> None:
        """Data does not require updates so we only need to fetch it if we don't already have it."""
        lazy_update(
            ConstituencyResultDetail,
            fetch_and_create_election_result,
            json_data,
            **kwargs,
        )

    update_model(
        endpoints.ELECTION_RESULTS,
        update_item_func=update_result_details,
        follow_pagination=follow_pagination,
        **kwargs,
    )
