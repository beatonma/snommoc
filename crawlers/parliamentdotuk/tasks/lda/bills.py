"""

"""

import logging
from typing import Optional

from celery import shared_task

from crawlers.parliamentdotuk.models import BillUpdateError
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import bills as contract
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_parliamentdotuk_id,
    get_item_data,
    unwrap_value_int,
    unwrap_str,
    unwrap_value_date,
    unwrap_value_str,
    update_model,
)
from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_str,
    coerce_to_list,
    coerce_to_boolean,
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
    session_data = data.get(contract.SESSION)
    if isinstance(session_data, list):
        session_data = session_data[0]

    parliamentdotuk = get_parliamentdotuk_id(session_data.get(contract.ABOUT))
    session, _ = ParliamentarySession.objects.get_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "name": session_data.get(contract.SESSION_NAME),
        },
    )
    return session


def _update_bill(parliamentdotuk: int, data: dict) -> Optional[str]:
    bill_type, _ = BillType.objects.get_or_create(
        name=coerce_to_str(data.get(contract.BILL_TYPE)),
        description=coerce_to_str(data.get(contract.BILL_TYPE_DESCRIPTION)),
    )

    bill, bill_created = Bill.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "act_name": coerce_to_str(data.get(contract.ACT_NAME)),
            "bill_chapter": coerce_to_str(data.get(contract.BILL_CHAPTER)),
            "bill_type": bill_type,
            "ballot_number": unwrap_value_int(data, contract.BALLOT_NUMBER),
            "date": unwrap_value_date(data, contract.DATE),
            "description": unwrap_str(data, contract.DESCRIPTION),
            "homepage": coerce_to_str(data.get(contract.HOMEPAGE)),
            "is_money_bill": coerce_to_boolean(data.get(contract.MONEY_BILL)),
            "is_private": coerce_to_boolean(data.get(contract.PRIVATE_BILL)),
            "label": unwrap_value_str(data, contract.LABEL),
            "public_involvement_allowed": coerce_to_boolean(
                data.get(contract.PUBLIC_INVOLVED)
            ),
            "session": _get_session(data),
            "title": coerce_to_str(data.get(contract.TITLE)),
        },
    )

    publications = coerce_to_list(data.get(contract.BILL_PUBLICATIONS))
    for pub in publications:
        _update_bill_publication(bill, pub)

    stages = coerce_to_list(data.get(contract.BILL_STAGES))
    for stage in stages:
        _update_bill_stage(bill, stage)

    sponsors = coerce_to_list(data.get(contract.SPONSORS))
    for sponsor in sponsors:
        _update_sponsor(bill, sponsor)

    if bill_created:
        return bill.title


def _update_bill_publication(bill, publication):
    pub_puk = get_parliamentdotuk_id(publication.get(contract.ABOUT))
    BillPublication.objects.update_or_create(
        parliamentdotuk=pub_puk,
        defaults={
            "bill": bill,
            "title": coerce_to_str(publication.get(contract.TITLE)),
        },
    )


def _update_bill_stage(bill, data: dict):
    parliamentdotuk = get_parliamentdotuk_id(data.get(contract.ABOUT))

    stage_type_data = data.get(contract.BILL_STAGE_TYPE)
    stage_type, _ = BillStageType.objects.get_or_create(
        parliamentdotuk=get_parliamentdotuk_id(stage_type_data.get(contract.ABOUT)),
        name=unwrap_value_str(stage_type_data, contract.LABEL),
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

    sittings = coerce_to_list(data.get(contract.BILL_STAGE_SITTINGS))
    for sitting in sittings:
        BillStageSitting.objects.get_or_create(
            parliamentdotuk=get_parliamentdotuk_id(sitting.get(contract.ABOUT)),
            defaults={
                "bill_stage": stage,
                "date": unwrap_value_date(sitting, contract.DATE),
                "formal": coerce_to_boolean(sitting.get(contract.FORMAL)),
                "provisional": coerce_to_boolean(sitting.get(contract.PROVISIONAL)),
            },
        )


def _update_sponsor(bill, data):
    sponsor_name = unwrap_str(data, contract.SPONSOR_NAME)

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
        parliamentdotuk = get_parliamentdotuk_id(json_data.get(contract.ABOUT))
        try:
            parliamentdotuk = get_parliamentdotuk_id(json_data.get(contract.ABOUT))

            data = get_item_data(endpoints.BILL.format(parliamentdotuk=parliamentdotuk))
            if data is None:
                return None

            return _update_bill(parliamentdotuk, data)
        except Exception as e:
            BillUpdateError.create(parliamentdotuk, e)
            raise e

    update_model(
        endpoints.BILLS,
        update_item_func=fetch_and_update_bill,
        follow_pagination=follow_pagination,
        **kwargs,
    )
