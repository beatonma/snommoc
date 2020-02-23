"""

"""

import logging

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda import divisions as tmod  # module under test

log = logging.getLogger(__name__)


class CommonsDivisionsTestCase(LocalTestCase):
    """"""
    def test_get_vote_commons_member_id(self):
        vote_data = {"_about": "http://data.parliament.uk/resources/1171292/vote/103", "member": [{"_about": "http://data.parliament.uk/members/4443", "label": {"_value": "Biography information for Carol Monaghan"}}], "memberParty": "Scottish National Party", "memberPrinted": {"_value": "Carol Monaghan"}, "type": "http://data.parliament.uk/schema/parl#AyeVote"}
        self.assertEqual(4443, tmod._get_vote_commons_member_id(vote_data))

    def test_get_vote_lords_member_id(self):
        vote_data = {"_about": "http://data.parliament.uk/resources/714002/vote/1", "member": ["http://data.parliament.uk/resources/members/api/lords/id/3898"], "memberParty": "Crossbench", "memberRank": "Lord", "memberTitle": "Aberdare", "type": "http://data.parliament.uk/schema/parl#ContentVote"}
        self.assertEqual(3898, tmod._get_vote_lords_member_id(vote_data))
