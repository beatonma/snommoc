from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.network import JsonCache, json_cache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.divisions import schema
from repository.models import Person
from repository.models.divisions import (
    DivisionVoteType,
    LordsDivision,
    LordsDivisionVote,
)


def update_lords_division(data_dict: dict, context: TaskContext) -> None:
    """Signature: openapi_client.ItemFunc"""
    data = schema.LordsDivision(**data_dict)

    sponsor = (
        Person.objects.get_member(data.sponsoringMemberId)
        if data.sponsoringMemberId
        else None
    )

    division, created = LordsDivision.objects.update_or_create(
        parliamentdotuk=data.divisionId,
        defaults={
            "title": data.title,
            "date": data.date,
            "number": data.number,
            "notes": data.notes,
            "is_whipped": data.isWhipped,
            "is_government_content": data.isGovernmentContent,
            "authoritative_content_count": data.authoritativeContentCount,
            "authoritative_not_content_count": data.authoritativeNotContentCount,
            "division_had_tellers": data.divisionHadTellers,
            "teller_content_count": data.tellerContentCount,
            "teller_not_content_count": data.tellerNotContentCount,
            "member_content_count": data.memberContentCount,
            "member_not_content_count": data.memberNotContentCount,
            "sponsoring_member": sponsor,
            "is_house": data.isHouse,
            "amendment_motion_notes": data.amendmentMotionNotes,
            "is_government_win": data.isGovernmentWin,
            "remote_voting_start": data.remoteVotingStart,
            "remote_voting_end": data.remoteVotingEnd,
            "division_was_exclusively_remote": data.divisionWasExclusivelyRemote,
        },
    )

    content, _ = DivisionVoteType.objects.get_or_create(name="content")
    not_content, _ = DivisionVoteType.objects.get_or_create(name="not_content")

    for vote in data.contents + data.contentTellers:
        person = Person.objects.get_member(vote.memberId, name=vote.name)
        LordsDivisionVote.objects.update_or_create(
            person=person,
            division=division,
            defaults={
                "vote_type": content,
            },
        )

    for vote in data.notContents + data.notContentTellers:
        person = Person.objects.get_member(vote.memberId, name=vote.name)
        LordsDivisionVote.objects.update_or_create(
            person=person,
            division=division,
            defaults={
                "vote_type": not_content,
            },
        )

    if created:
        context.info(f"Created LordsDivision '{division}'")


@json_cache(caches.LORDS_DIVISIONS)
def fetch_and_update_lords_division(
    parliamentdotuk: int,
    cache: JsonCache | None = None,
):
    context = TaskContext(cache=cache, notification=None)
    openapi_client.get(
        endpoints.lords_division(parliamentdotuk),
        update_lords_division,
        context=context,
    )


@task_context(cache_name=caches.LORDS_DIVISIONS)
def update_lords_divisions(
    context: TaskContext,
) -> None:
    openapi_client.foreach(
        endpoints.LORDS_DIVISIONS_ALL,
        item_func=update_lords_division,
        context=context,
    )
