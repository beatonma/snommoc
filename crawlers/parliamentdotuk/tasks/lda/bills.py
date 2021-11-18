import logging
from typing import Optional

from celery import shared_task

from crawlers.network import json_cache
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import bills as contract
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_boolean,
    get_date,
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
    Bill,
    BillPublication,
    BillSponsor,
    BillStage,
    BillStageSitting,
    BillStageType,
    BillType,
    ParliamentarySession,
)
from repository.resolution.members import get_member_by_name, normalize_name

log = logging.getLogger(__name__)


def _get_session(data: dict):
    check_required_fields(
        data,
        contract.SESSION,
    )

    session_data = data.get(contract.SESSION)
    if isinstance(session_data, list):
        session_data = session_data[0]

    check_required_fields(
        session_data,
        contract.ABOUT,
        contract.SESSION_NAME,
    )

    parliamentdotuk = get_parliamentdotuk_id(session_data)
    session, _ = ParliamentarySession.objects.get_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "name": session_data.get(contract.SESSION_NAME),
        },
    )
    return session


def _update_bill(parliamentdotuk: int, data: dict) -> Optional[str]:
    check_required_fields(
        data,
        contract.ABOUT,
        contract.TITLE,
        contract.DATE,
        contract.HOMEPAGE,
        contract.LABEL,
        contract.BILL_TYPE,
        contract.BILL_TYPE_DESCRIPTION,
    )

    bill_type, _ = BillType.objects.get_or_create(
        name=get_str(data, contract.BILL_TYPE),
        description=get_str(data, contract.BILL_TYPE_DESCRIPTION),
    )

    bill, bill_created = Bill.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "act_name": get_str(data, contract.ACT_NAME),
            "bill_chapter": get_str(data, contract.BILL_CHAPTER),
            "bill_type": bill_type,
            "ballot_number": get_int(data, contract.BALLOT_NUMBER, default=0),
            "date": get_date(data, contract.DATE),
            "description": get_str(data, contract.DESCRIPTION),
            "homepage": get_str(data, contract.HOMEPAGE),
            "is_money_bill": get_boolean(data, contract.MONEY_BILL),
            "is_private": get_boolean(data, contract.PRIVATE_BILL),
            "label": get_str(data, contract.LABEL),
            "public_involvement_allowed": get_boolean(data, contract.PUBLIC_INVOLVED),
            "session": _get_session(data),
            "title": get_str(data, contract.TITLE),
        },
    )

    publications = get_list(data, contract.BILL_PUBLICATIONS)
    for pub in publications:
        _update_bill_publication(bill, pub)

    stages = get_list(data, contract.BILL_STAGES)
    for stage in stages:
        _update_bill_stage(bill, stage)

    sponsors = get_list(data, contract.SPONSORS)
    for sponsor in sponsors:
        _update_sponsor(bill, sponsor)

    if bill_created:
        return bill.title


def _update_bill_publication(bill: Bill, data: dict):
    check_required_fields(
        data,
        contract.TITLE,
    )

    pub_puk = get_parliamentdotuk_id(data)
    BillPublication.objects.update_or_create(
        parliamentdotuk=pub_puk,
        defaults={
            "bill": bill,
            "title": get_str(data, contract.TITLE),
        },
    )


def _update_bill_stage(bill: Bill, data: dict):
    check_required_fields(
        data,
        contract.ABOUT,
        contract.BILL_STAGE_TYPE,
    )

    parliamentdotuk = get_parliamentdotuk_id(data)

    stage_type_data = data.get(contract.BILL_STAGE_TYPE)
    check_required_fields(
        stage_type_data,
        contract.ABOUT,
        contract.LABEL,
    )
    stage_type, _ = BillStageType.objects.get_or_create(
        parliamentdotuk=get_parliamentdotuk_id(stage_type_data),
        name=get_str(stage_type_data, contract.LABEL),
    )

    session = _get_session(data)

    stage, _ = BillStage.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "bill": bill,
            "bill_stage_type": stage_type,
            "session": session,
        },
    )

    sittings = get_list(data, contract.BILL_STAGE_SITTINGS)
    for sitting in sittings:
        BillStageSitting.objects.get_or_create(
            parliamentdotuk=get_parliamentdotuk_id(sitting),
            defaults={
                "bill_stage": stage,
                "date": get_date(sitting, contract.DATE),
                "formal": get_boolean(sitting, contract.FORMAL, default=False),
                "provisional": get_boolean(
                    sitting, contract.PROVISIONAL, default=False
                ),
            },
        )


def _update_sponsor(bill: Bill, data: dict):
    sponsor_name = get_str(data, contract.SPONSOR_NAME)
    normalized_name = normalize_name(sponsor_name)

    if not normalized_name:
        log.warning(
            f"Sponsor name is empty (bill:{bill.parliamentdotuk}): '{sponsor_name}' -> '{normalized_name}'"
        )
        return

    person = get_member_by_name(normalized_name)
    if person:
        BillSponsor.objects.get_or_create(
            name=normalized_name,
            person=person,
            bill=bill,
        )

    else:
        BillSponsor.objects.get_or_create(
            name=normalized_name,
            bill=bill,
        )


@shared_task
@task_notification(label="Update bills")
@json_cache(name="bills")
def update_bills(follow_pagination=True, **kwargs) -> None:
    def fetch_and_update_bill(json_data) -> Optional[str]:
        parliamentdotuk = get_parliamentdotuk_id(json_data)

        data = get_item_data(
            endpoints.url_for_bill(parliamentdotuk),
            cache=kwargs.get("cache"),
        )
        if data is not None:
            return _update_bill(parliamentdotuk, data)

    update_model(
        endpoints.BILLS,
        update_item_func=fetch_and_update_bill,
        follow_pagination=follow_pagination,
        **kwargs,
    )
