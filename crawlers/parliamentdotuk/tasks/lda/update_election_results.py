import logging
from typing import (
    Optional,
    Tuple,
)

from celery import shared_task

from crawlers.parliamentdotuk.models import ElectionResultUpdateError
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_int,
    get_item_data,
    get_list,
    get_nested_value,
    get_parliamentdotuk_id,
    get_str,
    unwrap_value_str,
    update_model,
)
from crawlers.parliamentdotuk.tasks.util.coercion import coerce_to_str
from repository.models import (
    Constituency,
    ConstituencyResult,
    Election,
)
from repository.models.election_result import (
    ConstituencyCandidate,
    ConstituencyResultDetail,
)
from crawlers.parliamentdotuk.tasks.lda.contract import electionresults as contract
from repository.models.util.queryset import get_or_none


log = logging.getLogger(__name__)


def _create_election_result(parliamentdotuk, data):
    constituency_id = get_parliamentdotuk_id(
        get_nested_value(data, contract.CONSTITUENCY_ABOUT))
    election_name = coerce_to_str(get_nested_value(data, contract.ELECTION_NAME))

    constituency = get_or_none(Constituency, parliamentdotuk=constituency_id)
    election, _ = Election.objects.get_or_create(name=election_name, defaults={
        'parliamentdotuk': get_parliamentdotuk_id(
            get_nested_value(data, contract.ELECTION_ABOUT))
    })

    try:
        constituency_result = ConstituencyResult.objects.get(
            election=election,
            constituency=constituency,
        )
    except Exception as e:
        log.warning(f'Could not retrieve ConstituencyResult: '
                    f'constituency={constituency}, election={election}')
        raise e

    electorate = get_int(data, contract.ELECTORATE)
    turnout = get_int(data, contract.TURNOUT)
    turnout_fraction = turnout / electorate

    result, _ = ConstituencyResultDetail.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            'constituency_result': constituency_result,
            'electorate': electorate,
            'majority': get_int(data, contract.MAJORITY),
            'result': get_str(data, contract.RESULT_OF_ELECTION),
            'turnout': turnout,
            'turnout_fraction': turnout_fraction,
        }
    )

    candidates = get_list(data, contract.CANDIDATES)
    for candidate in candidates:
        _create_candidate(result, candidate)


def _create_candidate(election_result, candidate):
    name = unwrap_value_str(candidate, contract.CANDIDATE_NAME)

    ConstituencyCandidate.objects.update_or_create(
        election_result=election_result,
        name=name,
        defaults={
            'votes': get_int(candidate, contract.CANDIDATE_VOTES),
            'order': get_int(candidate, contract.CANDIDATE_ORDINAL),
            'party': unwrap_value_str(candidate, contract.CANDIDATE_PARTY)
        }
    )


@shared_task
def update_election_results(follow_pagination=True) -> None:
    def update_result_details(json_data) -> Optional[str]:
        puk = get_parliamentdotuk_id(json_data.get(contract.ABOUT))

        try:
            ConstituencyResultDetail.objects.get(parliamentdotuk=puk)
        except ConstituencyResultDetail.DoesNotExist:
            return fetch_and_create_election_result(puk)

    def fetch_and_create_election_result(parliamentdotuk) -> Optional[str]:
        try:
            data = get_item_data(endpoints.ELECTION_RESULT_DETAIL.format(parliamentdotuk=parliamentdotuk))
            if data is None:
                return None

            return _create_election_result(parliamentdotuk, data)
        except Exception as e:
            ElectionResultUpdateError.create(parliamentdotuk, e)

    def build_report(new_results: list) -> Tuple[str, str]:
        return 'Election results updated', '\n'.join(new_results)

    update_model(
        endpoints.ELECTION_RESULTS,
        update_item_func=update_result_details,
        report_func=build_report,
        follow_pagination=follow_pagination,
        item_uses_network=True,
    )
