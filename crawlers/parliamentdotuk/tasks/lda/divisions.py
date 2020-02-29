"""

"""

import logging
from typing import (
    Optional,
    Tuple,
)

from celery import shared_task

from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    update_model,
    get_parliamentdotuk_id,
    get_item_data,
    unwrap_value_date,
    unwrap_value_int,
)

from crawlers.parliamentdotuk.tasks.lda.contract import divisions as contract
from crawlers.parliamentdotuk.tasks.lda.contract import votes as votes_contract
from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_int,
    coerce_to_str,
    coerce_to_boolean,
)
from repository.models.session import ParliamentarySession
from repository.models.divisions import (
    CommonsDivision,
    CommonsDivisionVote,
    LordsDivision,
    LordsDivisionVote,
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
        parliamentdotuk = get_parliamentdotuk_id(about_url)

        session, _ = ParliamentarySession.objects.get_or_create(
            parliamentdotuk=parliamentdotuk,
            name=date,
        )
    return session


def _get_vote_commons_member_id(vote_data):
    return get_parliamentdotuk_id(vote_data.get(contract.VOTE_MEMBER)[0].get(contract.ABOUT))


def _get_vote_lords_member_id(vote_data):
    return get_parliamentdotuk_id(vote_data.get(contract.VOTE_MEMBER)[0])


def _create_commons_division(parliamentdotuk: int, data: dict) -> Optional[str]:
    division = CommonsDivision.objects.create(
        parliamentdotuk=parliamentdotuk,
        title=coerce_to_str(data.get(contract.TITLE)),
        abstentions=unwrap_value_int(data, contract.ABSTENTIONS),
        ayes=unwrap_value_int(data, contract.AYES),
        noes=unwrap_value_int(data, contract.NOES),
        did_not_vote=unwrap_value_int(data, contract.DID_NOT_VOTE),
        non_eligible=unwrap_value_int(data, contract.NON_ELIGIBLE),
        errors=unwrap_value_int(data, contract.ERRORS),
        suspended_or_expelled=unwrap_value_int(data, contract.SUSPENDED_OR_EXPELLED),
        date=unwrap_value_date(data, contract.DATE),
        deferred_vote=coerce_to_boolean(data.get(contract.DEFERRED_VOTE)),
        session=_get_session(data),
        uin=data.get(contract.UIN),
        division_number=coerce_to_int(data.get(contract.DIVISION_NUMBER)),
    )

    division.save()

    votes = data.get(contract.VOTES)
    for vote in votes:
        vote_type = (coerce_to_str(vote.get(contract.VOTE_TYPE))
                     .replace('http://', '').replace('https://', ''))
        if vote_type not in {
            votes_contract.VOTE_AYE,
            votes_contract.VOTE_NO,
            votes_contract.VOTE_DID_NOT,
            votes_contract.VOTE_ABSTAINS,
            votes_contract.VOTE_SUSPENDED_EXPELLED,
        }:
            log.warning(f'Unhandled vote type: "{vote_type}"')

        CommonsDivisionVote.objects.update_or_create(
            division=division,
            person_id=_get_vote_commons_member_id(vote),
            aye=vote_type == votes_contract.VOTE_AYE,
            no=vote_type == votes_contract.VOTE_NO,
            abstention=vote_type == votes_contract.VOTE_ABSTAINS,
            did_not_vote=vote_type == votes_contract.VOTE_DID_NOT,
            suspended_or_expelled=vote_type == votes_contract.VOTE_SUSPENDED_EXPELLED,
        )

    return division.title


def _create_lords_division(parliamentdotuk: int, data: dict) -> Optional[str]:
    division = LordsDivision.objects.create(
        parliamentdotuk=parliamentdotuk,
        title=coerce_to_str(data.get(contract.TITLE)),
        description=coerce_to_str(data.get(contract.DESCRIPTION)[0]),
        ayes=coerce_to_int(data.get(contract.CONTENT)),
        noes=coerce_to_int(data.get(contract.NOT_CONTENT)),
        date=unwrap_value_date(data, contract.DATE),
        session=_get_session(data),
        uin=data.get(contract.UIN),
        division_number=coerce_to_int(data.get(contract.DIVISION_NUMBER)),
        whipped_vote=coerce_to_boolean(data.get(contract.WHIPPED_VOTE)),
    )

    division.save()

    votes = data.get(contract.VOTES)
    for vote in votes:
        vote_type = (coerce_to_str(vote.get(contract.VOTE_TYPE))
                     .replace('http://', '').replace('https://', ''))
        if vote_type not in {votes_contract.VOTE_CONTENT, votes_contract.VOTE_NOT_CONTENT}:
            log.warning(f'Unhandled vote type: "{vote_type}"')

        LordsDivisionVote.objects.update_or_create(
            division=division,
            person_id=_get_vote_lords_member_id(vote),
            aye=vote_type == votes_contract.VOTE_CONTENT,
            no=vote_type == votes_contract.VOTE_NOT_CONTENT,
        )

    return division.title


@shared_task
def update_commons_divisions(follow_pagination=True) -> None:
    def update_division(json_data) -> Optional[str]:
        puk = get_parliamentdotuk_id(json_data.get(contract.ABOUT))

        try:
            CommonsDivision.objects.get(parliamentdotuk=puk)
            # Already exists, no need to fetch further data
            return None
        except CommonsDivision.DoesNotExist:
            return fetch_and_create_division(puk)

    def fetch_and_create_division(parliamentdotuk) -> Optional[str]:
        data = get_item_data(endpoints.COMMONS_DIVISION.format(parliamentdotuk=parliamentdotuk))
        if data is None:
            return None

        return _create_commons_division(parliamentdotuk, data)

    def build_report(new_divisions: list) -> Tuple[str, str]:
        return 'Commons divisions updated', '\n'.join(new_divisions)

    update_model(
        endpoints.COMMONS_DIVISIONS,
        update_item_func=update_division,
        report_func=build_report,
        follow_pagination=follow_pagination,
    )


@shared_task
def update_lords_divisions(follow_pagination=True) -> None:
    def update_division(json_data) -> Optional[str]:
        puk = get_parliamentdotuk_id(json_data.get(contract.ABOUT))

        try:
            LordsDivision.objects.get(parliamentdotuk=puk)
            # Already exists, no need to fetch further data
            return None
        except LordsDivision.DoesNotExist:
            return fetch_and_create_division(puk)

    def fetch_and_create_division(parliamentdotuk) -> Optional[str]:
        data = get_item_data(endpoints.LORDS_DIVISION.format(parliamentdotuk=parliamentdotuk))
        if data is None:
            return None

        return _create_lords_division(parliamentdotuk, data)

    def build_report(new_divisions: list) -> Tuple[str, str]:
        return 'Lords divisions updated', '\n'.join(new_divisions)

    update_model(
        endpoints.LORDS_DIVISIONS,
        update_item_func=update_division,
        report_func=build_report,
        follow_pagination=follow_pagination,
    )


