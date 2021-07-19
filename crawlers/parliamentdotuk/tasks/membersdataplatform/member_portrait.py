"""

"""

import logging
import re
from typing import (
    Optional,
)

from django.db.models import QuerySet

from celery import shared_task

from common.network.rate_limit import rate_limit
from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints
from notifications.models.task_notification import task_notification
from repository.models import Person
from repository.models.portrait import MemberPortrait
from repository.resolution import get_active_members
from crawlers.network import get_json
from crawlers.wikipedia import wikipedia_client

log = logging.getLogger(__name__)


MEMBER_PORTRAIT_URL_PATTERN = re.compile(
    r"(https://members-api\.parliament\.uk/api/Members/[0-9]+/Portrait).*"
)
CROP_FULLSIZE = "FullSize"
CROP_SQUARE = "OneOne"
CROP_WIDE = "ThreeTwo"
CROP_TALL = "ThreeFour"


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


def _get_wikipedia_portraits(members: QuerySet[Person]):
    """
    Sample response:
        {
          "batchcomplete": "",
          "query": {
            "pages": {
              "414450": {
                "pageid": 414450,
                "ns": 0,
                "title": "John Baron (politician)",
                "original": {
                  "source": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Official_portrait_of_Mr_John_Baron_MP_crop_2.jpg",
                  "width": 1500,
                  "height": 2000
                }
              }
            }
          }
        }
    """
    print(f"Looking for portraits for {members.count()} members...")
    wiki_pages = [m.wikipedia for m in members if m.wikipedia]

    images_map = {}

    def get_main_image(name, data):
        if "original" in data:
            m = images_map.get(name, {})
            m["main"] = data["original"].get("source")
            images_map[name] = m

    def get_thumbnail(name, data):
        if "thumbnail" in data:
            m = images_map.get(name, {})
            m["thumbnail"] = data["thumbnail"].get("source")
            images_map[name] = m

    wikipedia_client.for_pages(
        wiki_pages,
        get_main_image,
        prop="pageimages",
        piprop="original",
    )

    wikipedia_client.for_pages(
        wiki_pages,
        get_thumbnail,
        prop="pageimages",
        pithumbsize=1000,
    )

    for p in members:
        images = images_map.get(p.wikipedia)
        if not images:
            continue

        main_url = images.get("main")
        thumbnail_url = images.get("thumbnail")

        MemberPortrait.objects.update_or_create(
            person=p,
            defaults={
                "fullsize_url": main_url,
                "square_url": thumbnail_url,
                "tall_url": thumbnail_url,
                "wide_url": thumbnail_url,
            },
        )


def _get_portrait_url(member_id: int, **kwargs) -> Optional[str]:
    try:
        data = get_json(endpoints.MEMBER_PORTRAIT_URL.format(id=member_id), **kwargs)
        return data.get("value")
    except Exception as e:
        log.warning(f"Could not get portrait url [{member_id}]: {e}")
        return None


def _update_member_portrait(member: Person, portrait_url: str):
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


@shared_task
@task_notification(label="UpdateMemberPortraits")
def update_member_portraits(**kwargs):
    active_members = get_active_members()

    for m in active_members:
        url = _get_portrait_url(m.parliamentdotuk, **kwargs)
        if url is not None:
            _update_member_portrait(m, url)

        rate_limit()

    members_without_portraits = get_active_members(memberportrait__isnull=True)
    log.info(
        f"There are {members_without_portraits.count()} active members with no official portrait."
    )

    _get_wikipedia_portraits(members_without_portraits)


@shared_task
@task_notification(label="UpdateWikipediaPortraits")
def update_missing_member_portraits_wikipedia(**kwargs):
    """
    Get portraits from wikipedia for members who have a confirmed wikipedia page but no portrait.
    :param kwargs:
    :return:
    """
    members = get_active_members(wikipedia__isnull=False, memberportrait__isnull=True)

    _get_wikipedia_portraits(members)


@shared_task
@task_notification(label="UpdateWikipediaPortraits")
def update_member_portraits_wikipedia(**kwargs):
    members = get_active_members(wikipedia__isnull=False)
    _get_wikipedia_portraits(members)
