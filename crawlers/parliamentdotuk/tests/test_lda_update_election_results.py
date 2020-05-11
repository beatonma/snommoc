"""

"""
import datetime
import logging

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda.update_election_results import _create_election_result
from crawlers.parliamentdotuk.tests.data_lda_update_election_results import ELECTION_RESULT_DETAIL
from repository.models import (
    Constituency,
    Election,
)
from repository.models.election_result import (
    ConstituencyCandidate,
    ElectionResult,
)

log = logging.getLogger(__name__)


class UpdateElectionResultsTests(LocalTestCase):
    """"""
    def setUp(self) -> None:
        Constituency.objects.create(
            parliamentdotuk=143474,
            name='Aberdeen North',
        ).save()

        Election.objects.create(
            parliamentdotuk=382037,
            name='2010 General Election',
            date=datetime.date.today(),
        ).save()

    def tearDown(self) -> None:
        self.delete_instances_of(
            Constituency,
            Election,
            ElectionResult,
            ConstituencyCandidate
        )

    def test_create_election_result(self):
        data = ELECTION_RESULT_DETAIL
        _create_election_result(382387, data)

        self.assertEqual(1, ElectionResult.objects.count())
        aberdeen_north: ElectionResult = ElectionResult.objects.first()
        self.assertEqual(aberdeen_north.turnout, 37701)
        self.assertEqual(aberdeen_north.majority, 8361)
        self.assertEqual(aberdeen_north.electorate, 64808)
        self.assertEqual(aberdeen_north.result, 'Lab Hold')
        self.assertAlmostEqual(
            float(aberdeen_north.turnout_fraction),
            0.58173,
            places=3
        )

        self.assertEqual(aberdeen_north.constituency.name, 'Aberdeen North')
        self.assertEqual(aberdeen_north.election.name, '2010 General Election')
