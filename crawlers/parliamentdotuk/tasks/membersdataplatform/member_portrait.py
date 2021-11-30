import logging
import re
from typing import Optional

from celery import shared_task
from django.db.models import QuerySet

from crawlers import caches
from crawlers.network import HttpNoContent, get_json, json_cache
from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints
from crawlers.wikipedia.tasks.member_portrait import update_wikipedia_member_portraits
from notifications.models.task_notification import task_notification
from repository.models import Person
from repository.models.portrait import MemberPortrait
from repository.resolution import get_active_members

log = logging.getLogger(__name__)


MEMBER_PORTRAIT_URL_PATTERN = re.compile(
    r"(https://members-api\.parliament\.uk/api/Members/[0-9]+/Portrait).*"
)
CROP_FULLSIZE = "FullSize"
CROP_SQUARE = "OneOne"
CROP_WIDE = "ThreeTwo"
CROP_TALL = "ThreeFour"


def _update_official_member_portrait(member: Person, portrait_url: str):
    """
    Update/create MemberPortrait from official API response.
    """

    def _url_with_croptype(base_url: str, croptype: str):
        return f"{base_url}?cropType={croptype}"

    base_url = MEMBER_PORTRAIT_URL_PATTERN.match(portrait_url).group(1)

    try:
        MemberPortrait.objects.update_or_create(
            person_id=member.parliamentdotuk,
            defaults={
                "fullsize_url": _url_with_croptype(base_url, CROP_FULLSIZE),
                "square_url": _url_with_croptype(base_url, CROP_SQUARE),
                "wide_url": _url_with_croptype(base_url, CROP_WIDE),
                "tall_url": _url_with_croptype(base_url, CROP_TALL),
            },
        )
    except:
        log.warning(f"Failed to update portrait data for member {member}")


@json_cache(caches.MEMBER_PORTRAITS)
def _update_official_member_portraits(members: QuerySet[Person], **kwargs):
    """Try to get portrait data from the official parliament.uk API for each given member."""

    def _get_portrait_url(member_id: int) -> Optional[str]:
        try:
            data = get_json(
                endpoints.MEMBER_PORTRAIT_URL.format(id=member_id), **kwargs
            )
            return data.get("value")
        except HttpNoContent:
            pass
        except Exception as e:
            log.warning(f"Could not get portrait url [{member_id}]: {e}")

    for m in members:
        url = _get_portrait_url(m.parliamentdotuk)
        if url is not None:
            _update_official_member_portrait(m, url)


@shared_task
@task_notification(label="UpdateMemberPortraits")
def update_member_portraits(**kwargs):
    active_members = get_active_members()

    _update_official_member_portraits(active_members, **kwargs)

    members_without_portraits = get_active_members(memberportrait__isnull=True)

    update_wikipedia_member_portraits(members_without_portraits)


@shared_task
@task_notification(label="UpdateWikipediaPortraits")
def update_missing_member_portraits_wikipedia(**kwargs):
    """
    Get portraits from wikipedia for members who have a confirmed wikipedia page but no portrait.
    """
    members = get_active_members(wikipedia__isnull=False, memberportrait__isnull=True)

    update_wikipedia_member_portraits(members)


@shared_task
@task_notification(label="UpdateWikipediaPortraits")
def update_member_portraits_wikipedia(**kwargs):
    members = get_active_members(wikipedia__isnull=False)
    update_wikipedia_member_portraits(members)


def update_member_portrait(member: Person):
    """Update an individual portrait"""

    as_queryset = Person.objects.filter(pk=member.pk)
    _update_official_member_portraits(as_queryset)

    try:
        MemberPortrait.objects.get(person=member)
    except MemberPortrait.DoesNotExist:
        update_wikipedia_member_portraits(as_queryset)
