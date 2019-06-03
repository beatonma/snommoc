from dataclasses import dataclass
from typing import Dict, Optional, List

import re
import requests

COMMONS_MEMBERS_BASE_URL = 'https://lda.data.parliament.uk/commonsmembers.json'
PARAM_PAGE_SIZE = '_pageSize'
PARAM_PAGE = '_page'
MAX_PAGE_SIZE = 500


def _get_value(d: Dict, key: str):
    v = d.get(key)
    if isinstance(v, str):
        return v
    elif isinstance(v, Dict):
        if '_value' in v.keys():
            return v.get('_value')
        elif 'label' in v.keys():
            return v.get('label').get('_value')


@dataclass
class MemberJsonItem:
    data: Dict

    def _get_value(self, key: str):
        v = self.data.get(key)
        if isinstance(v, str):
            return v
        elif isinstance(v, Dict):
            if '_value' in v.keys():
                return v.get('_value')
            elif 'label' in v.keys():
                return v.get('label').get('_value')

    def to_commons_member(self):
        return CommonsMember(
            parliamentdotuk_id=_get_parliamentdotuk_id(self.data),
            given_name=self._get_value('givenName'),
            family_name=self._get_value('familyName'),
            party=self._get_value('party'),
            constituency=self._get_value('constituency'),
            gender=self._get_value('gender'),
            home_page=self._get_value('homePage'),
            twitter=self._get_value('twitter')
        )


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


def _get_parliamentdotuk_id(person_json_item: Dict[str, str]) -> Optional[int]:
    matches = re.findall(r'.*?/([\d]+)$', person_json_item.get('_about'))
    if matches:
        return int(matches[0])


def get_page_json(page_number: int = 0, page_size: int = MAX_PAGE_SIZE):
    response = requests.get(
        COMMONS_MEMBERS_BASE_URL,
        params={
            PARAM_PAGE_SIZE: page_size,
            PARAM_PAGE: page_number
        })

    return response.json()


def create_members(json_items: List) -> List[CommonsMember]:
    return [MemberJsonItem(i).to_commons_member() for i in json_items]
