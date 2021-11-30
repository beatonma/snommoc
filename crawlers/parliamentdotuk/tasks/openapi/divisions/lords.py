from typing import Optional

from celery import shared_task

from crawlers import caches
from crawlers.network import JsonResponseCache, json_cache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.schema import DivisionViewModel
from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_date,
    coerce_to_datetime,
)
from notifications.models.task_notification import TaskNotification, task_notification
from repository.models.lords_division import (
    DivisionVoteType,
    LordsDivision,
    LordsDivisionVote,
)
from repository.resolution.members import get_member


def update_lords_division(
    data_dict: dict,
    notification: Optional[TaskNotification] = None,
) -> None:
    data = DivisionViewModel(**data_dict)

    sponsor = (
        get_member(pk=data.sponsoringMemberId) if data.sponsoringMemberId else None
    )

    division, created = LordsDivision.objects.update_or_create(
        parliamentdotuk=data.divisionId,
        defaults={
            "title": data.title,
            "date": coerce_to_date(data.date),
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
            "remote_voting_start": coerce_to_datetime(data.remoteVotingStart),
            "remote_voting_end": coerce_to_datetime(data.remoteVotingEnd),
            "division_was_exclusively_remote": data.divisionWasExclusivelyRemote,
        },
    )

    content, _ = DivisionVoteType.objects.get_or_create(name="content")
    not_content, _ = DivisionVoteType.objects.get_or_create(name="not_content")

    for vote in data.contents + data.contentTellers:
        person = get_member(pk=vote.memberId)
        LordsDivisionVote.objects.update_or_create(
            person=person,
            division=division,
            defaults={
                "vote_type": content,
            },
        )

    for vote in data.notContents + data.notContentTellers:
        person = get_member(pk=vote.memberId)
        LordsDivisionVote.objects.update_or_create(
            person=person,
            division=division,
            defaults={
                "vote_type": not_content,
            },
        )

    if created and notification:
        notification.append(f"Created LordsDivision '{division}'")


@json_cache(caches.LORDS_DIVISIONS)
def fetch_and_update_lords_division(
    parliamentdotuk: int,
    cache: Optional[JsonResponseCache] = None,
):
    openapi_client.get(
        endpoints.lords_division(parliamentdotuk),
        update_lords_division,
        notification=None,
        cache=cache,
    )


@shared_task
@task_notification(label="Update Lords divisions")
@json_cache(caches.LORDS_DIVISIONS)
def update_lords_divisions(
    cache: Optional[JsonResponseCache] = None,
    notification: Optional[TaskNotification] = None,
    **kwargs,
) -> None:
    openapi_client.foreach(
        endpoints.LORDS_DIVISIONS_ALL,
        item_func=update_lords_division,
        cache=cache,
        notification=notification,
    )
