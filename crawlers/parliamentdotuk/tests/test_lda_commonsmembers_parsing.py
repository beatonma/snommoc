"""

"""

import logging

from basetest.test_util import inject_context_manager
from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda.commons_members import (
    create_members,
    CommonsMember,
)

log = logging.getLogger(__name__)

EXAMPLE_MEMBER_JSON_ITEMS = [
    {
        "_about": "http://data.parliament.uk/members/172",
        "additionalName": {"_value": "Julie"},
        "constituency": {
            "_about": "http://data.parliament.uk/resources/146966",
            "label": {"_value": "Hackney North and Stoke Newington"},
        },
        "familyName": {"_value": "Abbott"},
        "fullName": {"_value": "Ms Diane Abbott"},
        "gender": {"_value": "Female"},
        "givenName": {"_value": "Diane"},
        "homePage": "http://www.dianeabbott.org.uk",
        "label": {"_value": "Biography information for Ms Diane Abbott"},
        "party": {"_value": "Labour"},
        "twitter": {"_value": "https://twitter.com/HackneyAbbott"},
    },
    {
        "_about": "http://data.parliament.uk/members/4212",
        "additionalName": {"_value": "Angela Elspeth Marie"},
        "constituency": {
            "_about": "http://data.parliament.uk/resources/147130",
            "label": {"_value": "Oldham East and Saddleworth"},
        },
        "familyName": {"_value": "Abrahams"},
        "fullName": {"_value": "Debbie Abrahams"},
        "gender": {"_value": "Female"},
        "givenName": {"_value": "Deborah"},
        "homePage": "http://www.debbieabrahams.org.uk/",
        "label": {"_value": "Biography information for Debbie Abrahams"},
        "party": {"_value": "Labour"},
        "twitter": {"_value": "https://twitter.com/Debbie_abrahams"},
    },
]

inject_context_manager(CommonsMember)


class TestCommonsMemberParsing(LocalTestCase):
    """"""

    def test_create_members(self):
        members = create_members(EXAMPLE_MEMBER_JSON_ITEMS)

        with members[0] as member:
            self.assertEqual(member.family_name, "Abbott")
            self.assertEqual(member.given_name, "Diane")
            self.assertEqual(member.gender, "Female")
            self.assertEqual(member.home_page, "http://www.dianeabbott.org.uk")
            self.assertEqual(member.party, "Labour")
            self.assertEqual(member.twitter, "https://twitter.com/HackneyAbbott")
            self.assertEqual(member.constituency, "Hackney North and Stoke Newington")

        with members[1] as member:
            self.assertEqual(member.family_name, "Abrahams")
            self.assertEqual(member.given_name, "Deborah")
            self.assertEqual(member.gender, "Female")
            self.assertEqual(member.home_page, "http://www.debbieabrahams.org.uk/")
            self.assertEqual(member.party, "Labour")
            self.assertEqual(member.twitter, "https://twitter.com/Debbie_abrahams")
            self.assertEqual(member.constituency, "Oldham East and Saddleworth")
