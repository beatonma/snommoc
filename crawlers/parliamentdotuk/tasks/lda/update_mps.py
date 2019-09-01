from typing import (
    Optional,
    Tuple,
)

import re

from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.contract import commonsmembers as mp_contract
from crawlers.parliamentdotuk.tasks.lda.util import (
    get_value,
    update_model,
)
from repository.models import (
    Mp,
    Party,
)


def update_mps():
    parties = Party.objects.all()

    def build_mp(json_data) -> Optional[str]:
        def _get_parliamentdotuk_id(url) -> Optional[int]:
            matches = re.findall(r'.*?/([\d]+)$', url)
            if matches:
                return int(matches[0])

        name = get_value(json_data, 'full_name')
        mp, created = Mp.objects.update_or_create(
            name=name,
            defaults={
                'name': name,
                'parliamentdotuk': _get_parliamentdotuk_id(get_value(json_data, mp_contract.ABOUT)),
                'given_name': get_value(json_data, mp_contract.NAME_GIVEN),
                'family_name': get_value(json_data, mp_contract.NAME_FAMILY),
                # ''party' TODO get from `parties` cache to avoid many lookups
                # 'constituency' TODO avoid many lookups
                # TODO handle contact details. this update_or_create thing might not work for this
                # TODO ... fill all fields
            }
        )

    def build_report(new_mps) -> Tuple[str, str]:
        title = 'MPs updated'
        if new_mps:
            mp_list_test = '\n  '.join(new_mps)
            content = f'{len(new_mps)} new MPs:\n{mp_list_test}'
        else:
            content = 'No new MPs'
        return title, content

    update_model(
        endpoints.COMMONS_MEMBERS_BASE_URL,
        update_item_func=build_mp,
        report_func=build_report)
