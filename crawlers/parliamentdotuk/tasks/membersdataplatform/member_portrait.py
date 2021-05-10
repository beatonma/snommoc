"""

"""

import logging
import re
import time
from typing import (
    Optional,
    List,
)

import requests
from celery import shared_task
from django.conf import settings

from common.network.rate_limit import rate_limit
from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints
from notifications.models.task_notification import task_notification
from repository.models import Person
from repository.models.portrait import MemberPortrait

log = logging.getLogger(__name__)


MEMBER_PORTRAIT_URL_PATTERN = re.compile(
    r"(https://members-api\.parliament\.uk/api/Members/[0-9]+/Portrait).*"
)
CROP_FULLSIZE = "FullSize"
CROP_SQUARE = "OneOne"
CROP_WIDE = "ThreeTwo"
CROP_TALL = "ThreeFour"


def _get(url: str):
    """Get the url using our standard headers."""
    response = requests.get(url, headers=settings.HTTP_REQUEST_HEADERS)
    return response


def _update_official_portraits(csv_data: str):
    lines = csv_data.splitlines()
    for line in lines[1:]:
        parliamentdotuk, _name, _, _, year_taken, full, wide, tall, square = line.split(
            ","
        )

        try:
            Person.objects.get(parliamentdotuk=parliamentdotuk)
            MemberPortrait.objects.update_or_create(
                person_id=int(parliamentdotuk),
                defaults={
                    "year_taken": int(year_taken),
                    "fullsize_url": full,
                    "wide_url": wide,
                    "tall_url": tall,
                    "square_url": square,
                },
            )
        except Exception as e:
            log.warning(f"Unknown person {_name} id={parliamentdotuk}: {e}")


def _get_wikipedia_portraits(members: List[Person]):
    raise NotImplementedError("TODO: Try to find member photo from Wikipedia api")


def _get_portrait_url(member_id: int) -> Optional[str]:
    try:
        result = _get(endpoints.MEMBER_PORTRAIT_URL.format(id=member_id))
        if result.status_code == 200:
            return result.json().get("value")
    except:
        return None


def _url_with_croptype(base_url: str, croptype: str):
    return f"{base_url}?cropType={croptype}"


def _update_member_portrait(member: Person, portrait_url: str):
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


@shared_task
@task_notification(label="UpdateMemberPortraits")
def update_member_portraits(**kwargs):
    active_members = Person.objects.filter(active=True)

    for m in active_members:
        url = _get_portrait_url(m.parliamentdotuk)
        if url is not None:
            _update_member_portrait(m, url)

        rate_limit()

    members_without_portraits = Person.objects.filter(
        active=True, memberportrait__isnull=True
    )
    log.info(
        f"There are {members_without_portraits.count()} active members with no official portrait."
    )

    _get_wikipedia_portraits(members_without_portraits)
