from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from repository.models import House, Organisation, ParliamentarySession
from repository.models.bill import (
    Bill,
    BillAgent,
    BillSponsor,
    BillStage,
    BillStageType,
    BillType,
)


def _get_agent(api_bill: schema.Bill) -> BillAgent | None:
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


def _get_current_stage(api_bill: schema.Bill, db_bill: Bill) -> BillStage:
    stage = api_bill.currentStage
    stage_type = BillStageType.objects.get(parliamentdotuk=stage.stageId)
    house, _ = House.objects.get_or_create(name=stage.house.name)

    session, _ = ParliamentarySession.objects.get_or_create(
        parliamentdotuk=stage.sessionId
    )

    current_stage, _ = BillStage.objects.update_or_create(
        parliamentdotuk=stage.id,
        defaults={
            "bill": db_bill,
            "description": stage.description,
            "abbreviation": stage.abbreviation,
            "house": house,
            "session": session,
            "sort_order": stage.sortOrder,
            "stage_type": stage_type,
        },
    )
    return current_stage


def _get_sponsors(api_bill: schema.Bill) -> list[BillSponsor]:
    return [
        _get_sponsor(api_bill.billId, sponsor)
        for sponsor in api_bill.sponsors
        if sponsor is not None
    ]


def _get_sponsor(bill_id: int, api_sponsor: schema.Sponsor) -> BillSponsor | None:
    organisation = None
    if api_sponsor.organisation:
        organisation, _ = Organisation.objects.update_or_create(
            name=api_sponsor.organisation.name,
            defaults={
                "url": api_sponsor.organisation.url,
            },
        )

    member_id = api_sponsor.member.memberId if api_sponsor.member else None
    if member_id:
        db_sponsor, _ = BillSponsor.objects.update_or_create(
            member_id=member_id,
            bill_id=bill_id,
            defaults={
                "organisation": organisation,
                "sort_order": api_sponsor.sortOrder,
            },
        )

    elif organisation:
        db_sponsor, _ = BillSponsor.objects.update_or_create(
            bill_id=bill_id,
            member_id=None,
            organisation=organisation,
            defaults={
                "sort_order": api_sponsor.sortOrder,
            },
        )

    else:
        # Neither member nor organisation provided.
        return None

    return db_sponsor


def _get_promoters(api_bill: schema.Bill) -> list[Organisation]:
    promoters = []
    for promoter in api_bill.promoters:
        organisation, _ = Organisation.objects.update_or_create(
            name=promoter.organisationName,
            defaults={
                "url": promoter.organisationUrl,
            },
        )
        promoters.append(organisation)

    return promoters


def update_bill(data: dict, context: TaskContext) -> None:
    """Signature: openapi_client.ItemFunc"""
    api_bill = schema.Bill(**data)

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
            "withdrawn_at": api_bill.billWithdrawn,
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
