import datetime
from unittest import mock

import requests

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda import endpoints, lda_client
from crawlers.parliamentdotuk.tasks.lda.divisions import (
    _create_commons_division,
    _create_commons_vote,
    _get_vote_commons_member_id,
    _get_vote_lords_member_id,
    update_commons_divisions,
)
from crawlers.parliamentdotuk.tests.data_lda_divisions import (
    EXAMPLE_COMMONS_DIVISION,
    EXAMPLE_COMMONS_DIVISIONS_LIST,
    EXAMPLE_COMMONS_DIVISION_COMPLETE,
    EXAMPLE_COMMONS_VOTE,
    EXAMPLE_COMMONS_VOTE_AYE,
    EXAMPLE_COMMONS_VOTE_NO,
    EXAMPLE_LORDS_VOTE,
)
from crawlers.parliamentdotuk.tests.mock import MockJsonResponse
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    LordsDivision,
    LordsDivisionVote,
)


class CommonsDivisionsTestCase(LocalTestCase):
    """ """

    def test_get_vote_commons_member_id(self):
        data = EXAMPLE_COMMONS_VOTE
        self.assertEqual(4443, _get_vote_commons_member_id(data))

    def test_get_vote_lords_member_id(self):
        data = EXAMPLE_LORDS_VOTE
        self.assertEqual(3898, _get_vote_lords_member_id(data))

    def test_create_commons_vote_aye(self):
        data = EXAMPLE_COMMONS_VOTE_AYE

        _create_commons_vote(1171292, data)
        vote: CommonsDivisionVote = CommonsDivisionVote.objects.first()
        self.assertTrue(vote.aye)
        self.assertFalse(vote.no)
        self.assertFalse(vote.suspended_or_expelled)
        self.assertFalse(vote.did_not_vote)
        self.assertFalse(vote.abstention)

    def test_create_commons_vote_no(self):
        data = EXAMPLE_COMMONS_VOTE_NO

        _create_commons_vote(1171292, data)
        vote: CommonsDivisionVote = CommonsDivisionVote.objects.first()
        self.assertTrue(vote.no)
        self.assertFalse(vote.aye)
        self.assertFalse(vote.suspended_or_expelled)
        self.assertFalse(vote.did_not_vote)
        self.assertFalse(vote.abstention)

    def test_create_commons_division(self):
        data = EXAMPLE_COMMONS_DIVISION

        _create_commons_division(1171292, data)

        division: CommonsDivision = CommonsDivision.objects.get(parliamentdotuk=1171292)
        self.assertEqual(division.ayes, 222)
        self.assertEqual(division.noes, 313)
        self.assertEqual(division.margin, 91)
        self.assertEqual(division.abstentions, 0)
        self.assertEqual(division.non_eligible, 0)
        self.assertEqual(division.errors, 0)
        self.assertEqual(division.did_not_vote, 0)
        self.assertEqual(division.suspended_or_expelled, 0)
        self.assertEqual(division.division_number, 15)
        self.assertEqual(division.session.name, "2017/19")
        self.assertEqual(division.session.parliamentdotuk, 730830)
        self.assertEqual(
            division.title, "The Queen's Speech: Jeremy Corbyn's amendment (c) "
        )
        self.assertEqual(division.uin, "CD:2020-01-16:750")
        self.assertEqual(division.date, datetime.date(year=2020, month=1, day=16))

        self.assertFalse(division.deferred_vote)

        self.assertLengthEquals(division.votes.all(), 55)

    def tearDown(self) -> None:
        self.delete_instances_of(
            CommonsDivision,
            CommonsDivisionVote,
            LordsDivision,
            LordsDivisionVote,
        )


def get_mock_divisions(*args, **kwargs):
    url = args[0].url
    if url.startswith(endpoints.COMMONS_DIVISIONS + "?"):
        response = EXAMPLE_COMMONS_DIVISIONS_LIST
    else:
        response = EXAMPLE_COMMONS_DIVISION_COMPLETE
    return MockJsonResponse(url, response, 200)


class MockCommonsDivisionTestCase(LocalTestCase):
    """ """

    @mock.patch.object(
        requests.Session,
        "send",
        mock.Mock(side_effect=get_mock_divisions),
    )
    @mock.patch.object(
        lda_client, "_get_next_page_url", mock.Mock(side_effect=lambda x: None)
    )
    def test_update_commons_divisions(self):
        update_commons_divisions(follow_pagination=False, cache=None)
        division = CommonsDivision.objects.first()

        self.assertEqual(
            division.title,
            "Opposition day debate on tax avoidance and evasion: Mr Corbyn's motion ",
        )
        self.assertEqual(division.uin, "CD:2020-02-25:770")
        self.assertEqual(division.date, datetime.date(year=2020, month=2, day=25))

        self.assertEqual(division.ayes, 236)
        self.assertEqual(division.noes, 322)
        self.assertEqual(division.margin, 86)

    def tearDown(self) -> None:
        self.delete_instances_of(
            CommonsDivision,
            CommonsDivisionVote,
            LordsDivision,
            LordsDivisionVote,
        )
