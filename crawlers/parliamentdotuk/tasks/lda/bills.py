"""

"""

import logging
from typing import Optional

from celery import shared_task

from crawlers.parliamentdotuk.models import BillUpdateError
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import bills as contract
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_boolean,
    get_date,
    get_int,
    get_list,
    get_parliamentdotuk_id,
    get_item_data,
    get_str,
    update_model,
)
from crawlers.parliamentdotuk.tasks.util.checks import (
    MissingFieldException,
    check_required_fields,
)
from notifications.models.task_notification import task_notification

from repository.models import (
    Bill,
    BillPublication,
    BillType,
    ParliamentarySession,
    Person,
    BillSponsor,
    BillStage,
    BillStageType,
    BillStageSitting,
)
from repository.models.person import PersonAlsoKnownAs
from crawlers.parliamentdotuk.tasks.network import json_cache

log = logging.getLogger(__name__)


def _get_session(data):
    check_required_fields(
        data,
        [
            contract.SESSION,
        ],
    )

    session_data = data.get(contract.SESSION)
    if isinstance(session_data, list):
        session_data = session_data[0]

    check_required_fields(
        session_data,
        [
            contract.ABOUT,
            contract.SESSION_NAME,
        ],
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
        [
            contract.ABOUT,
            contract.BILL_TYPE,
            contract.BILL_TYPE_DESCRIPTION,
            contract.DATE,
            contract.ACT_NAME,
            contract.BILL_CHAPTER,
            contract.BALLOT_NUMBER,
            contract.DATE,
            contract.DESCRIPTION,
            contract.HOMEPAGE,
            contract.MONEY_BILL,
            contract.PRIVATE_BILL,
            contract.LABEL,
            contract.PUBLIC_INVOLVED,
            contract.TITLE,
            contract.BILL_PUBLICATIONS,
            contract.BILL_STAGES,
            contract.SPONSORS,
        ],
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
            "ballot_number": get_int(data, contract.BALLOT_NUMBER),
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


def _update_bill_publication(bill, publication):
    check_required_fields(
        publication,
        [
            contract.ABOUT,
            contract.TITLE,
        ],
    )

    pub_puk = get_parliamentdotuk_id(publication)
    BillPublication.objects.update_or_create(
        parliamentdotuk=pub_puk,
        defaults={
            "bill": bill,
            "title": get_str(publication, contract.TITLE),
        },
    )


def _update_bill_stage(bill, data: dict):
    check_required_fields(
        data,
        [
            contract.ABOUT,
            contract.BILL_STAGE_TYPE,
            contract.BILL_STAGE_SITTINGS,
        ],
    )

    parliamentdotuk = get_parliamentdotuk_id(data)

    stage_type_data = data.get(contract.BILL_STAGE_TYPE)
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
                "formal": get_boolean(sitting, contract.FORMAL),
                "provisional": get_boolean(sitting, contract.PROVISIONAL),
            },
        )


def _update_sponsor(bill, data):
    sponsor_name = get_str(data, contract.SPONSOR_NAME)

    try:
        person = Person.objects.get(name=sponsor_name)
        BillSponsor.objects.get_or_create(
            person=person,
            bill=bill,
        )
        return

    except Person.MultipleObjectsReturned:
        BillSponsor.objects.get_or_create(
            name=sponsor_name,
            bill=bill,
        )
        return

    except Person.DoesNotExist:
        pass

    try:
        # Check if we have registered any aliases that match the name.
        alias = PersonAlsoKnownAs.objects.get(alias=sponsor_name)
        BillSponsor.objects.get_or_create(
            person=alias.person,
            bill=bill,
        )
        return
    except PersonAlsoKnownAs.DoesNotExist:
        BillSponsor.objects.get_or_create(
            name=sponsor_name,
            bill=bill,
        )


@shared_task
@task_notification(label="Update bills")
@json_cache(name="bills")
def update_bills(follow_pagination=True, **kwargs) -> None:
    def fetch_and_update_bill(json_data) -> Optional[str]:
        parliamentdotuk = get_parliamentdotuk_id(json_data)
        try:
            data = get_item_data(endpoints.url_for_bill(parliamentdotuk))
            if data is not None:
                return _update_bill(parliamentdotuk, data)

        except MissingFieldException as e:
            raise e

        except Exception as e:
            BillUpdateError.create(parliamentdotuk, e)
            raise e

    update_model(
        endpoints.BILLS,
        update_item_func=fetch_and_update_bill,
        follow_pagination=follow_pagination,
        **kwargs,
    )
