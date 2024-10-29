from datetime import date

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.membersdataplatform import schema

from . import testdata


class MemberSchemaTest(LocalTestCase):

    def test_members_list_schema(self):
        members = schema.MemberListResponse.model_validate(testdata.MemberList).members

        member = members[0]

        self.assertTrue(member.is_active)
        self.assertEqual(member.parliamentdotuk, 172)
        self.assertEqual(member.name, "Ms Diane Abbott")
        self.assertEqual(member.house, "Commons")
        self.assertEqual(member.constituency_name, "Hackney North and Stoke Newington")

    def test_member_full_biography_schema(self):
        biog = schema.MemberResponse.model_validate(testdata.MemberFullBiog).member

        self.assertTrue(biog.is_active)
        self.assertEqual(biog.parliamentdotuk, 4514)
        self.assertEqual(biog.name, "Sir Keir Starmer")
        self.assertEqual(biog.party.name, "Labour")
        self.assertIsNone(biog.date_of_birth)
        self.assertIsNone(biog.date_of_death)
        self.assertEqual(biog.house_start_date, date(2015, 5, 7))

        address = biog.addresses[0]
        self.assertTrue(address.is_physical)
        self.assertEqual(address.type, "Parliamentary office")
        self.assertEqual(address.address, "House of Commons, London")

        twitter = biog.addresses[1]
        self.assertFalse(twitter.is_physical)
        self.assertEqual(twitter.type, "X (formerly Twitter)")
        self.assertEqual(twitter.address, "https://twitter.com/keir_starmer")
