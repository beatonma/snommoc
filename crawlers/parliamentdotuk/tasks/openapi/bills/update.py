from typing import List, Optional

from crawlers.parliamentdotuk.tasks.openapi.bills import viewmodels
from notifications.models import TaskNotification
from repository.models import House, Organisation, ParliamentarySession
from repository.models.bill import (
    Bill,
    BillAgent,
    BillSponsor,
    BillStage,
    BillStageType,
    BillType,
)


def _get_agent(api_bill: viewmodels.Bill) -> Optional[BillAgent]:
    agent = None
    if api_bill.agent is not None:
        _agent = api_bill.agent
        agent, _ = BillAgent.objects.update_or_create(
            name=_agent.name,
            defaults={
                "address": _agent.address,
                "phone_number": _agent.phoneNo,
                "email": _agent.email,
                "website": _agent.website,
            },
        )

    return agent


def _get_current_stage(api_bill: viewmodels.Bill, db_bill: Bill) -> BillStage:
    stage = api_bill.currentStage
    stage_type = BillStageType.objects.get(parliamentdotuk=stage.stageId)
    house, _ = House.objects.get_or_create(name=stage.house.name)

    current_stage, _ = BillStage.objects.update_or_create(
        parliamentdotuk=stage.id,
        defaults={
            "bill": db_bill,
            "description": stage.description,
            "abbreviation": stage.abbreviation,
            "house": house,
            "session_id": stage.sessionId,
            "sort_order": stage.sortOrder,
            "stage_type": stage_type,
        },
    )
    return current_stage


def _get_sponsors(api_bill: viewmodels.Bill) -> List[BillSponsor]:
    sponsors = []
    for sponsor in api_bill.sponsors:
        organisation = None
        if sponsor.organisation:
            organisation, _ = Organisation.objects.update_or_create(
                name=sponsor.organisation.name,
                defaults={
                    "url": sponsor.organisation.url,
                },
            )

        x, _ = BillSponsor.objects.update_or_create(
            bill_id=api_bill.billId,
            member_id=sponsor.member.memberId,
            organisation=organisation,
            sort_order=sponsor.sortOrder,
        )
        sponsors.append(x)

    return sponsors


def _get_promoters(api_bill: viewmodels.Bill) -> List[Organisation]:
    promoters = []
    for promoter in api_bill.promoters:
        organisation, _ = Organisation.objects.update_or_create(
            name=promoter.organisationName, defaults={"url": promoter.organisationUrl}
        )
        promoters.append(organisation)
    return promoters


def _update_bill(data: dict, notification: Optional[TaskNotification]) -> None:
    api_bill = viewmodels.Bill(**data)

    current_house, _ = House.objects.get_or_create(name=api_bill.currentHouse.name)
    originating_house, _ = House.objects.get_or_create(
        name=api_bill.originatingHouse.name
    )
    bill_type, _ = BillType.objects.get_or_create(parliamentdotuk=api_bill.billTypeId)
    session_introduced, _ = ParliamentarySession.objects.get_or_create(
        parliamentdotuk=api_bill.introducedSessionId
    )

    db_bill, _ = Bill.objects.update_or_create(
        parliamentdotuk=api_bill.billId,
        defaults={
            "title": api_bill.shortTitle,
            "long_title": api_bill.longTitle,
            "summary": api_bill.summary,
            "current_house": current_house,
            "originating_house": originating_house,
            "last_update": api_bill.lastUpdate,
            "date_withdrawn": api_bill.billWithdrawn,
            "is_defeated": api_bill.isDefeated,
            "is_act": api_bill.isAct,
            "bill_type": bill_type,
            "session_introduced": session_introduced,
        },
    )

    included_sessions = ParliamentarySession.objects.filter(
        parliamentdotuk__in=api_bill.includedSessionIds
    )
    db_bill.sessions.set(included_sessions)

    db_bill.current_stage = _get_current_stage(api_bill, db_bill)
    db_bill.agent = _get_agent(api_bill)
    db_bill.sponsors.set(_get_sponsors(api_bill))
    db_bill.promoters.set(_get_promoters(api_bill))

    db_bill.save()
