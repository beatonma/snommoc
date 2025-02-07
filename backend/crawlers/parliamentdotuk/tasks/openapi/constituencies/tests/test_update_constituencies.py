from datetime import date

from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks import (
    update_constituencies,
    update_constituency_boundaries,
    update_election_results,
)
from crawlers.parliamentdotuk.tasks.openapi.testcase import OpenApiTestCase
from notifications.models import TaskNotification
from repository.models import (
    Constituency,
    ConstituencyCandidate,
    ConstituencyResult,
    ConstituencyResultDetail,
)

CONTEXT = TaskContext(None, TaskNotification(), follow_pagination=False)


class _BaseTestCase(OpenApiTestCase):
    file = __file__
    mock_response = {
        "https://members-api.parliament.uk/api/Location/Constituency/Search": "data/constituencies.json",
        "https://members-api.parliament.uk/api/Location/Constituency/4483": "data/constituency-4483.json",
        "https://members-api.parliament.uk/api/Location/Constituency/4483/Geometry": "data/constituency-4483_geometry.json",
        "https://members-api.parliament.uk/api/Location/Constituency/4483/ElectionResults": "data/constituency-4483_electionresults.json",
        "https://members-api.parliament.uk/api/Location/Constituency/4483/ElectionResult/422": "data/constituency-4483_electionresult-422.json",
    }

    @classmethod
    def setUpTestData(cls):
        update_constituencies(context=CONTEXT)

    def setUp(self):
        self.constituency = Constituency.objects.get(parliamentdotuk=4483)


class UpdateConstituenciesTest(_BaseTestCase):
    def test_update_constituencies(self):
        con = self.constituency

        self.assertEqual(con.name, "Inverness, Skye and West Ross-shire")
        self.assertEqual(con.start, date(2024, 5, 31))
        self.assertEqual(con.mp.name, "Angus MacDonald")
        self.assertEqual(con.mp.party.name, "Liberal Democrat")


class UpdateConstituencyBoundariesTest(_BaseTestCase):
    def assertAlmostEqual(self, first, second, places=2, msg=None, delta=None):
        super().assertAlmostEqual(first, second, places=places, msg=msg, delta=delta)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        update_constituency_boundaries(context=CONTEXT)

    def test_update_constituency_boundaries(self):
        boundary = self.constituency.boundary

        self.assertAlmostEqual(boundary.centroid.x, -5.286)
        self.assertAlmostEqual(boundary.centroid.y, 57.253)
        self.assertAlmostEqual(boundary.north, 57.875)
        self.assertAlmostEqual(boundary.south, 56.708)
        self.assertAlmostEqual(boundary.east, -3.843)
        self.assertAlmostEqual(boundary.west, -6.789)


class UpdateElectionResultsTest(_BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        update_election_results(context=CONTEXT)

    def test_update_election_results(self):
        result: ConstituencyResult = self.constituency.results.get(election__pk=422)

        self.assertEqual(result.election.name, "2024 General Election")
        self.assertEqual(result.election.date, date(2024, 7, 4))

        self.assertEqual(result.winner.name, "Angus MacDonald")

        detail: ConstituencyResultDetail = result.detail
        self.assertEqual(detail.result, "gain")

        hendry: ConstituencyCandidate = detail.candidates.get(name="Drew Hendry")
        self.assertEqual(hendry.votes, 15999)
        self.assertEqual(hendry.order, 2)
        self.assertEqual(hendry.party.name, "Scottish National Party")
        self.assertEqual(hendry.result_change, "-15.4%")
