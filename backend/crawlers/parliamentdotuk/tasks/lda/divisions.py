import logging

from celery import shared_task
from crawlers import caches
from crawlers.context import TaskContext
from crawlers.network import JsonCache, json_cache
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.lda_client import get_item_data
from notifications.models.task_notification import TaskNotification, task_notification
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    DivisionVoteType,
    ParliamentarySession,
)

from . import lda_client
from . import schema as lda_schema

log = logging.getLogger(__name__)


def _get_session(data: lda_schema.division.Session):
    if data.parliamentdotuk:
        session, _ = ParliamentarySession.objects.get_or_create(
            parliamentdotuk=data.parliamentdotuk, defaults={"name": data.name}
        )
    else:
        session = ParliamentarySession.objects.get_or_none(name=data.name)

    return session


def _create_commons_vote(division_id: int, vote: lda_schema.Vote):
    if not isinstance(vote, lda_schema.Vote):
        raise Exception(f"Not a Vote instance: {vote}")

    vote_type, _ = DivisionVoteType.objects.get_or_create(name=vote.type)

    CommonsDivisionVote.objects.update_or_create(
        division_id=division_id,
        person_id=vote.member_parliamentdotuk,
        defaults={
            "vote_type": vote_type,
        },
    )


def _create_commons_division(
    parliamentdotuk: int, data: lda_schema.CommonsDivision
) -> None:
    division, _ = CommonsDivision.objects.update_or_create(
        parliamentdotuk=parliamentdotuk,
        defaults={
            "title": data.title,
            "abstentions": data.abstentions,
            "ayes": data.ayes,
            "noes": data.noes,
            "did_not_vote": data.did_not_vote,
            "non_eligible": data.non_eligible,
            "errors": data.errors,
            "suspended_or_expelled": data.suspended_or_expelled,
            "date": data.date,
            "deferred_vote": data.deferred_vote,
            "session": _get_session(data.session),
            "uin": data.uin,
            "division_number": data.division_number,
        },
    )

    for vote in data.votes:
        _create_commons_vote(division.parliamentdotuk, vote)


def fetch_and_create_commons_division(
    parliamentdotuk: int,
    context: TaskContext,
) -> None:
    data = get_item_data(
        type=lda_schema.CommonsDivision,
        endpoint=endpoints.url_for_commons_division(parliamentdotuk),
        context=context,
    )

    _create_commons_division(parliamentdotuk, data)


@shared_task
@task_notification(label="Update Commons divisions")
@json_cache(caches.COMMONS_DIVISIONS)
def update_commons_divisions(
    follow_pagination=True,
    cache: JsonCache | None = None,
    notification: TaskNotification | None = None,
    force_update: bool = False,
    skip: int = 0,
) -> None:
    context = TaskContext(notification=notification, cache=cache)

    def update_division(
        data: lda_schema.CommonsDivision, _context: TaskContext
    ) -> None:
        if (
            not force_update
            and CommonsDivision.objects.filter(
                parliamentdotuk=data.parliamentdotuk
            ).exists()
        ):
            return

        fetch_and_create_commons_division(
            data.parliamentdotuk,
            context=_context,
        )

    lda_client.foreach(
        endpoints.COMMONS_DIVISIONS,
        lda_schema.CommonsDivisionItem,
        item_func=update_division,
        context=context,
        follow_pagination=follow_pagination,
        skip=skip,
    )
