from dataclasses import dataclass
from typing import Dict, Optional, List

import re
import requests

COMMONS_MEMBERS_BASE_URL = 'https://lda.data.parliament.uk/commonsmembers.json'
PARAM_PAGE_SIZE = '_pageSize'
PARAM_PAGE = '_page'
MAX_PAGE_SIZE = 500


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

    def _get_value(key: str):
        v = data.get(key)
        if isinstance(v, str):
            return v
        elif isinstance(v, Dict):
            if '_value' in v.keys():
                return v.get('_value')
            elif 'label' in v.keys():
                return v.get('label').get('_value')

    return CommonsMember(
        parliamentdotuk_id=_get_parliamentdotuk_id(_get_value('_about')),
        given_name=_get_value('givenName'),
        family_name=_get_value('familyName'),
        party=_get_value('party'),
        constituency=_get_value('constituency'),
        gender=_get_value('gender'),
        home_page=_get_value('homePage'),
        twitter=_get_value('twitter')
    )


def create_members(json_items: List) -> List[CommonsMember]:
    return [build_commons_member(i) for i in json_items]


def get_page_json(page_number: int = 0, page_size: int = MAX_PAGE_SIZE):
    response = requests.get(
        COMMONS_MEMBERS_BASE_URL,
        params={
            PARAM_PAGE_SIZE: page_size,
            PARAM_PAGE: page_number
        })

    return response.json()


def get_all_mps() -> List[CommonsMember]:
    # TODO
    return []
