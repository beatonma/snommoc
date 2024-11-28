from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.divisions import schema
from crawlers.parliamentdotuk.tasks.openapi.divisions.shared import create_votes
from repository.models import Person
from repository.models.divisions import LordsDivision, LordsDivisionVote


@task_context(cache_name=caches.LORDS_DIVISIONS, items_per_page=10)
def update_lords_divisions(context: TaskContext) -> None:
    openapi_client.foreach(
        endpoints.LORDS_DIVISIONS_ALL,
        item_func=_update_lords_division,
        context=context,
    )


def _update_lords_division(response_data: dict, context: TaskContext) -> None:
    """Signature: openapi_client.ItemFunc"""
    data = schema.LordsDivision.model_validate(response_data)

    sponsor = (
        Person.objects.resolve(data.sponsoring_member_id)
        if data.sponsoring_member_id
        else None
    )

    division, created = LordsDivision.objects.update_or_create(
        parliamentdotuk=data.division_id,
        defaults={
            "title": data.title,
            "date": data.date,
            "number": data.number,
            "notes": data.notes,
            "is_whipped": data.is_whipped,
            "is_government_content": data.is_government_content,
            "authoritative_content_count": data.authoritative_content_count,
            "authoritative_not_content_count": data.authoritative_not_content_count,
            "is_passed": (
                data.authoritative_content_count > data.authoritative_not_content_count
            ),
            "division_had_tellers": data.division_had_tellers,
            "teller_content_count": data.teller_content_count,
            "teller_not_content_count": data.teller_not_content_count,
            "member_content_count": data.member_content_count,
            "member_not_content_count": data.member_not_content_count,
            "sponsoring_member": sponsor,
            "is_house": data.is_house,
            "amendment_motion_notes": data.amendment_motion_notes,
            "is_government_win": data.is_government_win,
        },
    )

    create_votes(division, LordsDivisionVote, data.contents, "content")
    create_votes(division, LordsDivisionVote, data.not_contents, "not_content")
    create_votes(
        division,
        LordsDivisionVote,
        data.content_tellers,
        "content",
        is_teller=True,
    )
    create_votes(
        division,
        LordsDivisionVote,
        data.not_content_tellers,
        "not_content",
        is_teller=True,
    )

    if created:
        context.info(f"Created LordsDivision '{division}'")
