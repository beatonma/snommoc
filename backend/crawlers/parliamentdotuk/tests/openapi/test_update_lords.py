import datetime

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.openapi.divisions.lords import \
    update_lords_division
from crawlers.parliamentdotuk.tests.openapi.data_lordsdivision import \
    LORDS_DIVISION_DATA
from repository.models import Person
from repository.models.lords_division import (DivisionVoteType, LordsDivision,
                                              LordsDivisionVote)
from repository.resolution.members import get_member
from repository.tests.data.create import create_sample_person
from util.time import tzdatetime


class UpdateLordsDivisionsTests(LocalTestCase):
    def setUp(self) -> None:
        create_sample_person(
            parliamentdotuk=1557,
            name="Baroness Kramer",
        )
        create_sample_person(
            parliamentdotuk=457,
            name="Lord Pendry",
        )
        create_sample_person(
            parliamentdotuk=2758,
            name="Lord Falconer of Thoroton",
        )
        create_sample_person(
            parliamentdotuk=395,
            name="Lord Blunkett",
        )
        create_sample_person(
            parliamentdotuk=3329,
            name="Lord Brougham and Vaux",
        )
        create_sample_person(
            parliamentdotuk=3799,
            name="Lord James of Blackheath",
        )
        data = LORDS_DIVISION_DATA

        update_lords_division(data, notification=None)

    def test_division_is_created(self):
        self.assertEqual(LordsDivision.objects.count(), 1)

    def test_division_fields_are_correct(self):
        division: LordsDivision = LordsDivision.objects.first()

        self.assertEqual(division.pk, 2613)
        self.assertEqual(division.title, "Dormant Assets Bill [HL]")
        self.assertEqual(division.number, 2)
        self.assertEqual(division.date, datetime.date(2021, 11, 16))
        self.assertEqual(division.notes, None)
        self.assertEqual(division.is_whipped, True)
        self.assertEqual(division.is_government_content, False)
        self.assertEqual(division.authoritative_content_count, 164)
        self.assertEqual(division.authoritative_not_content_count, 192)
        self.assertEqual(division.division_had_tellers, False)
        self.assertEqual(division.teller_content_count, 164)
        self.assertEqual(division.teller_not_content_count, 192)
        self.assertEqual(division.member_content_count, 164)
        self.assertEqual(division.member_not_content_count, 192)
        self.assertEqual(division.sponsoring_member_id, 1557)
        self.assertEqual(division.is_house, True)
        self.assertEqual(
            division.amendment_motion_notes,
            "<p>Baroness Kramer moved amendment 6, in clause 29, page 22, line 20, at"
            " end to insert—<br />“(3A) An order under this section may not be made"
            " unless the Secretary of State has certified that dormant account money"
            " will be used to fund projects, or aspects of project, for which funds"
            " would be unlikely to be made available by a Government department.”<br"
            " />The House divided:</p>",
        )
        self.assertEqual(division.is_government_win, True)
        self.assertEqual(
            division.remote_voting_start,
            tzdatetime(2021, 11, 16, 17, 49, 37),
        )
        self.assertEqual(
            division.remote_voting_end,
            tzdatetime(2021, 11, 16, 17, 59, 37),
        )
        self.assertEqual(division.division_was_exclusively_remote, True)

    def test_division_votes_are_correct(self):
        division: LordsDivision = LordsDivision.objects.first()
        votes = division.votes_redux

        self.assertEqual(votes.count(), 5)
        self.assertEqual(votes.filter(vote_type__name="content").count(), 3)
        self.assertEqual(votes.filter(vote_type__name="not_content").count(), 2)

    def test_person_votes_related_name_is_correct(self):
        votes = get_member(pk=2758).lords_division_votes

        self.assertEqual(votes.count(), 1)
        self.assertEqual(votes.first().vote_type.name, "content")

    def tearDown(self):
        self.delete_instances_of(
            DivisionVoteType,
            LordsDivision,
            LordsDivisionVote,
            Person,
        )
