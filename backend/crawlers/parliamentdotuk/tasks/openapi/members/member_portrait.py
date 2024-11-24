import logging
import re
from typing import Optional

from crawlers.context import TaskContext
from crawlers.network import get_json
from crawlers.network.exceptions import HttpNoContent
from crawlers.parliamentdotuk.tasks.openapi import endpoints
from django.db.models import QuerySet
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


def _update_official_member_portrait(
    member: Person, portrait_url: str, context: TaskContext
):
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
        context.info(f"Updated member portrait for {member}")
    except:
        log.warning(f"Failed to update portrait data for member {member}")


def update_official_member_portraits(members: QuerySet[Person], context: TaskContext):
    """Try to get portrait data from the official parliament.uk API for each given member."""

    def _get_portrait_url(member_id: int) -> Optional[str]:
        try:
            data = get_json(
                endpoints.member_portrait(member_id),
                cache=context.cache,
                session=context.session,
            )
            return data.get("value")
        except HttpNoContent:
            pass
        except Exception as e:
            log.warning(f"Could not get portrait url [{member_id}]: {e}")

    for m in members:
        url = _get_portrait_url(m.parliamentdotuk)
        if url is not None:
            _update_official_member_portrait(m, url, context)
