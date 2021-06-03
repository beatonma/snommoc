"""

"""

import logging
from typing import Optional

from celery import shared_task

from crawlers.parliamentdotuk.models import (
    CommonsDivisionUpdateError,
    LordsDivisionUpdateError,
)
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_boolean,
    get_date,
    get_int,
    get_list,
    get_parliamentdotuk_id,
    get_str,
    update_model,
    parse_parliamentdotuk_id,
    get_item_data,
)

from crawlers.parliamentdotuk.tasks.lda.contract import divisions as contract
from crawlers.parliamentdotuk.tasks.lda.contract import votes as votes_contract
from notifications.models.task_notification import task_notification
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    LordsDivision,
    LordsDivisionVote,
    ParliamentarySession,
)
from crawlers.parliamentdotuk.tasks.network import json_cache

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
            name=date,
        )
    return session


def _get_vote_commons_member_id(vote_data):
    return get_parliamentdotuk_id(vote_data.get(contract.VOTE_MEMBER)[0])


def _get_vote_lords_member_id(vote_data):
    return parse_parliamentdotuk_id(vote_data.get(contract.VOTE_MEMBER)[0])


def _create_commons_vote(division_id, vote):
    vote_type = get_str(vote, contract.VOTE_TYPE).split("#")[1]

    CommonsDivisionVote.objects.update_or_create(
        division_id=division_id,
        person_id=_get_vote_commons_member_id(vote),
        defaults={
            "aye": vote_type == votes_contract.VOTE_AYE,
            "no": vote_type == votes_contract.VOTE_NO,
            "abstention": vote_type == votes_contract.VOTE_ABSTAINS,
            "did_not_vote": vote_type == votes_contract.VOTE_DID_NOT,
            "suspended_or_expelled": vote_type
            == votes_contract.VOTE_SUSPENDED_EXPELLED,
        },
    )


def _create_lords_vote(division_id, vote):
    vote_type = get_str(vote, contract.VOTE_TYPE).split("#")[1]

    LordsDivisionVote.objects.update_or_create(
        division_id=division_id,
        person_id=_get_vote_lords_member_id(vote),
        defaults={
            "aye": vote_type == votes_contract.VOTE_CONTENT,
            "no": vote_type == votes_contract.VOTE_NOT_CONTENT,
        },
    )


def _create_commons_division(parliamentdotuk: int, data: dict) -> None:
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


def _create_lords_division(parliamentdotuk: int, data: dict) -> None:
    division, _ = LordsDivision.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "title": get_str(data, contract.TITLE),
            "description": get_str(data, contract.DESCRIPTION[0]),
            "ayes": get_int(data, contract.CONTENT),
            "noes": get_int(data, contract.NOT_CONTENT),
            "date": get_date(data, contract.DATE),
            "session": _get_session(data),
            "uin": get_str(data, contract.UIN),
            "division_number": get_int(data, contract.DIVISION_NUMBER),
            "whipped_vote": get_boolean(data, contract.WHIPPED_VOTE),
        },
    )

    votes = get_list(data, contract.VOTES)
    for vote in votes:
        _create_lords_vote(division.parliamentdotuk, vote)


@shared_task
@task_notification(label="Update all divisions")
@json_cache("divisions")
def update_all_divisions(follow_pagination=True, **kwargs) -> None:
    update_commons_divisions(follow_pagination)
    update_lords_divisions(follow_pagination)


@shared_task
@task_notification(label="Update Commons divisions")
@json_cache("divisions")
def update_commons_divisions(follow_pagination=True, **kwargs) -> None:
    def update_division(json_data) -> Optional[str]:
        puk = get_parliamentdotuk_id(json_data)

        try:
            CommonsDivision.objects.get(parliamentdotuk=puk)
            # Already exists, no need to fetch further data
            return None
        except CommonsDivision.DoesNotExist:
            fetch_and_create_division(puk)

    def fetch_and_create_division(parliamentdotuk) -> Optional[str]:
        try:
            data = get_item_data(endpoints.url_for_commons_division(parliamentdotuk))
            if data is None:
                return None

            _create_commons_division(parliamentdotuk, data)
        except Exception as e:
            CommonsDivisionUpdateError.create(parliamentdotuk, e)

    update_model(
        endpoints.COMMONS_DIVISIONS,
        update_item_func=update_division,
        follow_pagination=follow_pagination,
        **kwargs,
    )


@shared_task
@task_notification(label="Update Lords divisions")
@json_cache("divisions")
def update_lords_divisions(follow_pagination=True, **kwargs) -> None:
    def update_division(json_data) -> Optional[str]:
        puk = parse_parliamentdotuk_id(json_data.get(contract.ABOUT))

        try:
            LordsDivision.objects.get(parliamentdotuk=puk)
            # Already exists, no need to fetch further data
            return None
        except LordsDivision.DoesNotExist:
            return fetch_and_create_division(puk)

    def fetch_and_create_division(parliamentdotuk) -> Optional[str]:
        try:
            data = get_item_data(endpoints.url_for_lords_division(parliamentdotuk))
            if data is None:
                return None

            return _create_lords_division(parliamentdotuk, data)

        except Exception as e:
            LordsDivisionUpdateError.create(parliamentdotuk, e)

    update_model(
        endpoints.LORDS_DIVISIONS,
        update_item_func=update_division,
        follow_pagination=follow_pagination,
        **kwargs,
    )
