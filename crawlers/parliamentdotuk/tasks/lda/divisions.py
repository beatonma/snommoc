import logging
from typing import Optional

from celery import shared_task

from crawlers import caches
from crawlers.network import JsonResponseCache, json_cache
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import (
    divisions as contract,
    votes as votes_contract,
)
from crawlers.parliamentdotuk.tasks.lda.lazy_update import lazy_update
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_boolean,
    get_date,
    get_int,
    get_item_data,
    get_parliamentdotuk_id,
    get_str,
    parse_parliamentdotuk_id,
    update_model,
)
from crawlers.parliamentdotuk.tasks.util.checks import check_required_fields
from notifications.models.task_notification import task_notification
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    ParliamentarySession,
)

log = logging.getLogger(__name__)


def _get_session(data):
    session_data = data.get(contract.SESSION)
    if len(session_data) == 1:
        date = session_data
        try:
            session = ParliamentarySession.objects.get(
                name=date,
            )
        except ParliamentarySession.DoesNotExist:
            return None

    else:
        date, about_url = session_data
        parliamentdotuk = parse_parliamentdotuk_id(about_url)

        session, _ = ParliamentarySession.objects.get_or_create(
            parliamentdotuk=parliamentdotuk,
            defaults={
                "name": date,
            },
        )
    return session


def _get_vote_commons_member_id(vote_data):
    return get_parliamentdotuk_id(vote_data.get(contract.VOTE_MEMBER)[0])


def _get_vote_lords_member_id(vote_data):
    return parse_parliamentdotuk_id(vote_data.get(contract.VOTE_MEMBER)[0])


def _create_commons_vote(division_id, vote):
    vote_type = get_str(vote, contract.VOTE_TYPE).split("#")[1]
    person_id = _get_vote_commons_member_id(vote)

    if person_id is None:
        log.warning(f"Vote member ID is invalid: {vote}")
        return

    CommonsDivisionVote.objects.update_or_create(
        division_id=division_id,
        person_id=person_id,
        defaults={
            "aye": vote_type == votes_contract.VOTE_AYE,
            "no": vote_type == votes_contract.VOTE_NO,
            "abstention": vote_type == votes_contract.VOTE_ABSTAINS,
            "did_not_vote": vote_type == votes_contract.VOTE_DID_NOT,
            "suspended_or_expelled": vote_type
            == votes_contract.VOTE_SUSPENDED_EXPELLED,
        },
    )


def _create_commons_division(parliamentdotuk: int, data: dict) -> None:
    check_required_fields(
        data,
        contract.TITLE,
        contract.DATE,
        contract.DIVISION_NUMBER,
        contract.UIN,
    )

    division, _ = CommonsDivision.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "title": get_str(data, contract.TITLE),
            "abstentions": get_int(data, contract.ABSTENTIONS),
            "ayes": get_int(data, contract.AYES),
            "noes": get_int(data, contract.NOES),
            "did_not_vote": get_int(data, contract.DID_NOT_VOTE),
            "non_eligible": get_int(data, contract.NON_ELIGIBLE),
            "errors": get_int(data, contract.ERRORS),
            "suspended_or_expelled": get_int(data, contract.SUSPENDED_OR_EXPELLED),
            "date": get_date(data, contract.DATE),
            "deferred_vote": get_boolean(data, contract.DEFERRED_VOTE),
            "session": _get_session(data),
            "uin": data.get(contract.UIN),
            "division_number": get_int(data, contract.DIVISION_NUMBER),
        },
    )

    votes = data.get(contract.VOTES)
    for vote in votes:
        _create_commons_vote(division.parliamentdotuk, vote)


def fetch_and_create_commons_division(
    parliamentdotuk: int,
    cache: Optional[JsonResponseCache],
    **kwargs,
) -> None:
    data = get_item_data(
        endpoints.url_for_commons_division(parliamentdotuk),
        cache=cache,
    )
    if data is None:
        return None

    _create_commons_division(parliamentdotuk, data)


@shared_task
@task_notification(label="Update Commons divisions")
@json_cache(caches.COMMONS_DIVISIONS)
def update_commons_divisions(follow_pagination=True, **kwargs) -> None:
    def update_division(json_data) -> None:
        """By default, only fetch data from network if we do not already have data about this division.
        Use -force in management command to force update of already fetched data."""
        lazy_update(
            CommonsDivision,
            fetch_and_create_commons_division,
            json_data,
            **kwargs,
        )

    update_model(
        endpoints.COMMONS_DIVISIONS,
        update_item_func=update_division,
        follow_pagination=follow_pagination,
        **kwargs,
    )
