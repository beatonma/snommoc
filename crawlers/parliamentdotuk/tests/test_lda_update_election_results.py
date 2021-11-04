from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda.update_election_results import (
    _create_election_result,
)
from crawlers.parliamentdotuk.tests.data_lda_update_election_results import (
    ELECTION_RESULT_DETAIL,
)
from repository.models import (
    Constituency,
    ConstituencyResult,
    Election,
    PartyAlsoKnownAs,
    Person,
)
from repository.models.election_result import (
    ConstituencyCandidate,
    ConstituencyResultDetail,
)
from util.time import get_today


class UpdateElectionResultsTests(LocalTestCase):
    """"""

    def setUp(self) -> None:
        Constituency.objects.create(
            parliamentdotuk=143474,
            name="Aberdeen North",
        )

        Election.objects.create(
            parliamentdotuk=382037,
            name="2010 General Election",
            date=get_today(),
        )

        Person.objects.create(
            parliamentdotuk=1423,
            name="Boris Johnson",
            active=True,
        )

        ConstituencyResult.objects.create(
            election_id=382037, constituency_id=143474, mp_id=1423
        )

    def tearDown(self) -> None:
        self.delete_instances_of(
            Constituency,
            Election,
            ConstituencyResultDetail,
            ConstituencyCandidate,
            ConstituencyResult,
            Person,
            PartyAlsoKnownAs,
        )

    def test_create_election_result(self):
        data = ELECTION_RESULT_DETAIL
        _create_election_result(382387, data)

        self.assertEqual(1, ConstituencyResultDetail.objects.count())
        aberdeen_north: ConstituencyResultDetail = (
            ConstituencyResultDetail.objects.first()
        )
        self.assertEqual(aberdeen_north.turnout, 37701)
        self.assertEqual(aberdeen_north.majority, 8361)
        self.assertEqual(aberdeen_north.electorate, 64808)
        self.assertEqual(aberdeen_north.result, "Lab Hold")
        self.assertAlmostEqual(
            float(aberdeen_north.turnout_fraction), 0.58173, places=3
        )

        self.assertEqual(
            aberdeen_north.constituency_result.constituency.name, "Aberdeen North"
        )
        self.assertEqual(
            aberdeen_north.constituency_result.election.name, "2010 General Election"
        )
