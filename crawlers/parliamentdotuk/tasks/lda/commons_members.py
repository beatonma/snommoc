from dataclasses import dataclass
from typing import Dict, Optional, List

import re
from crawlers.parliamentdotuk.tasks.lda.util import get_value


@dataclass
class CommonsMember:
    parliamentdotuk_id: int
    given_name: str
    family_name: str
    party: str
    constituency: str
    gender: str
    home_page: str
    twitter: str


def build_commons_member(data: Dict) -> CommonsMember:
    def _get_parliamentdotuk_id(url) -> Optional[int]:
        matches = re.findall(r'.*?/([\d]+)$', url)
        if matches:
            return int(matches[0])

    return CommonsMember(
        parliamentdotuk_id=_get_parliamentdotuk_id(get_value(data, '_about')),
        given_name=get_value(data, 'givenName'),
        family_name=get_value(data, 'familyName'),
        party=get_value(data, 'party'),
        constituency=get_value(data, 'constituency'),
        gender=get_value(data, 'gender'),
        home_page=get_value(data, 'homePage'),
        twitter=get_value(data, 'twitter')
    )


def create_members(json_items: List) -> List[CommonsMember]:
    return [build_commons_member(i) for i in json_items]


def get_all_mps() -> List[CommonsMember]:
    # TODO
    return []
