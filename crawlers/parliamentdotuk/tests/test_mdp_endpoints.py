"""

"""

import logging

from basetest.testcase import LocalTestCase

log = logging.getLogger(__name__)

from crawlers.parliamentdotuk.tasks.membersdataplatform import endpoints


class MdpEndpointTests(LocalTestCase):
    """Ensure that endpoints for the Members Data Platform API are correct."""
    def test_all_mps_endpoint(self):
        self.assertEquals(
            endpoints.COMMONS_MEMBERS_ALL,
            'https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons|membership=all/'
        )

    def test_all_lords_endpoint(self):
        self.assertEquals(
            endpoints.LORDS_MEMBERS_ALL,
            'https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Lords|membership=all/'
        )

    def test_member_profile_endpoint(self):
        self.assertEquals(
            endpoints.member_biography(parliamentdotuk=172),
            'https://data.parliament.uk/membersdataplatform/services/mnis/members/query/id=172/FullBiog/'
        )
