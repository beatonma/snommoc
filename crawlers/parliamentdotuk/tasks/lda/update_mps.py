from typing import (
    Optional,
    Tuple,
)

import logging

from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import commonsmembers as mp_contract
from crawlers.parliamentdotuk.tasks.lda.lda_client import (
    get_value,
    update_model,
    get_parliamentdotuk_id,
)
from repository.models import (
    Mp,
    Party,
    Constituency,
)
from repository.models.contact_details import (
    Links,
    WebLink,
)
from repository.models.person import Person

log = logging.getLogger(__name__)


def update_mps(follow_pagination=True):
    parties = Party.objects.all()
    constituencies = Constituency.objects.all()

    def build_mp(json_data) -> Optional[str]:
        name = get_value(json_data, mp_contract.NAME_FULL)
        puk = get_parliamentdotuk_id(get_value(json_data, mp_contract.ABOUT))
        person, _ = Person.objects.update_or_create(name=name, defaults={
            'name': name,
            'given_name': get_value(json_data, mp_contract.NAME_GIVEN),
            'family_name': get_value(json_data, mp_contract.NAME_FAMILY),
            'additional_name': get_value(json_data, mp_contract.NAME_ADDITIONAL),
            'gender': get_value(json_data, mp_contract.GENDER),
        })
        mp, _ = Mp.objects.update_or_create(
            parliamentdotuk=puk,
            defaults={
                'person': person,
                'parliamentdotuk': puk,
                'party': parties.get_or_create(name=get_value(json_data, mp_contract.PARTY))[0],
            }
        )
        constituency, _ = constituencies.update_or_create(
            name=get_value(json_data, mp_contract.CONSTITUENCY),
            defaults={
                'mp': mp,
            })

        contact_details, _ = Links.objects.get_or_create(person=person)
        weblinks = [
            get_value(json_data, mp_contract.TWITTER),
            get_value(json_data, mp_contract.HOMEPAGE),
        ]
        for url in [x for x in weblinks if x]:
            WebLink.objects.update_or_create(
                url=url,
                defaults={
                    'links': contact_details,
                    'url': url,
                }
            )
        return mp

    def build_report(new_mps) -> Tuple[str, str]:
        title = 'MPs updated'
        if new_mps:
            mp_list_test = '\n'.join([x.__str__() for x in new_mps])
            content = f'{len(new_mps)} new MPs:\n{mp_list_test}'
        else:
            content = 'No new MPs'
        return title, content

    update_model(
        endpoints.COMMONS_MEMBERS_BASE_URL,
        update_item_func=build_mp,
        report_func=build_report,
        follow_pagination=follow_pagination)
