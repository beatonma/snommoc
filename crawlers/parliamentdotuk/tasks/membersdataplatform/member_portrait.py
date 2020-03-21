"""

"""

import logging
from typing import (
    Optional,
    List,
)

import requests
from celery import shared_task
from django.conf import settings

from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints
from repository.models import Person
from repository.models.portrait import MemberPortrait

log = logging.getLogger(__name__)


def _get(url: str):
    """Get the url using our standard headers and fix response encoding."""
    response = requests.get(url, headers=settings.HTTP_REQUEST_HEADERS)
    response.encoding = "utf-8-sig"
    return response


def _get_official_portraits_data() -> Optional[str]:
    try:
        return _get(endpoints.MEMBER_PORTRAITS).text
    except Exception:
        return None


def _update_official_portraits(csv_data: str):
    lines = csv_data.splitlines()
    for line in lines[1:]:
        parliamentdotuk, _name, _, _, year_taken, full, wide, tall, square = line.split(",")

        try:
            Person.objects.get(parliamentdotuk=parliamentdotuk)
            MemberPortrait.objects.update_or_create(
                person_id=int(parliamentdotuk),
                defaults={
                    'year_taken': int(year_taken),
                    'fullsize_url': full,
                    'wide_url': wide,
                    'tall_url': tall,
                    'square_url': square,
                }
            )
        except Exception as e:
            log.warning(f'Unknown person {_name} id={parliamentdotuk}: {e}')


def _get_wikipedia_portraits(members: List[Person]):
    raise NotImplementedError('TODO: Try to find member photo from Wikipedia api')


@shared_task
def update_member_portraits():
    data = _get_official_portraits_data()
    _update_official_portraits(data)

    members_without_portraits = Person.objects.filter(memberportrait__isnull=True)
    _get_wikipedia_portraits(members_without_portraits)
