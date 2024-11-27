from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from repository.models import House, Organisation, ParliamentarySession, Party, Person
from repository.models.bill import (
    Bill,
    BillAgent,
    BillSponsor,
    BillStage,
    BillStageType,
    BillType,
)


def update_bill(response_data: dict, context: TaskContext) -> None:
    """Signature: openapi_client.ItemFunc"""
    data = schema.Bill.model_validate(response_data)

    current_house, _ = House.objects.get_or_create(name=data.current_house.name)
    originating_house, _ = House.objects.get_or_create(name=data.originating_house.name)

    bill_type = BillType.objects.get(parliamentdotuk=data.bill_type_id)
    session_introduced, _ = ParliamentarySession.objects.get_or_create(
        parliamentdotuk=data.introduced_session_id
    )

    bill, _ = Bill.objects.update_or_create(
        parliamentdotuk=data.bill_id,
        defaults={
            "title": data.short_title,
            "long_title": data.long_title,
            "summary": data.summary,
            "current_house": current_house,
            "originating_house": originating_house,
            "last_update": data.last_update,
            "withdrawn_at": data.bill_withdrawn,
            "is_defeated": data.is_defeated,
            "is_act": data.is_act,
            "bill_type": bill_type,
            "session_introduced": session_introduced,
        },
    )

    included_sessions = ParliamentarySession.objects.filter(
        parliamentdotuk__in=data.included_session_ids
    )
    bill.sessions.set(included_sessions)

    # bill.current_stage = _get_current_stage(data, bill)
    bill.agent = _get_agent(data)
    bill.save()

    bill.promoters.set(_get_promoters(data))
    _add_sponsors(bill, data)


def _get_agent(data: schema.Bill) -> BillAgent | None:
    agent = None
    if data.agent is not None:
        _agent = data.agent
        agent, _ = BillAgent.objects.update_or_create(
            name=_agent.name,
            defaults={
                "address": _agent.address,
                "phone_number": _agent.phone,
                "email": _agent.email,
                "website": _agent.website,
            },
        )

    return agent


# def _get_current_stage(data: schema.Bill, bill: Bill) -> BillStage:
#     stage = data.current_stage
#     stage_type = BillStageType.objects.get(parliamentdotuk=stage.stage_id)
#     house, _ = House.objects.get_or_create(name=stage.house.name)
#
#     session, _ = ParliamentarySession.objects.get_or_create(
#         parliamentdotuk=stage.session_id
#     )
#
#     current_stage, _ = BillStage.objects.update_or_create(
#         parliamentdotuk=stage.id,
#         defaults={
#             "bill": bill,
#             "description": stage.description,
#             "abbreviation": stage.abbreviation,
#             "house": house,
#             "session": session,
#             "sort_order": stage.sort_order,
#             "stage_type": stage_type,
#         },
#     )
#     return current_stage


def _add_sponsors(bill: Bill, data: schema.Bill):
    for sponsor in data.sponsors:
        _get_sponsor(bill, sponsor)


def _get_sponsor(bill: Bill, data: schema.Sponsor):
    organisation = None
    if data.organisation:
        organisation, _ = Organisation.objects.update_or_create(
            name=data.organisation.name,
            defaults={
                "url": data.organisation.url,
            },
        )

    if member := data.member:
        party = Party.objects.get_or_none(name=member.party)
        person = Person.objects.get_member(
            member.member_id,
            name=member.name,
            defaults={"party": party},
        )

        sponsor, _ = BillSponsor.objects.update_or_create(
            member=person,
            bill=bill,
            defaults={
                "organisation": organisation,
                "sort_order": data.sort_order,
            },
        )

    elif organisation:
        sponsor, _ = BillSponsor.objects.update_or_create(
            bill=bill,
            member_id=None,
            organisation=organisation,
            defaults={
                "sort_order": data.sort_order,
            },
        )


def _get_promoters(data: schema.Bill) -> list[Organisation]:
    promoters = []
    for promoter in data.promoters:
        organisation, _ = Organisation.objects.update_or_create(
            name=promoter.organisation_name,
            defaults={
                "url": promoter.organisation_url,
            },
        )
        promoters.append(organisation)

    return promoters
