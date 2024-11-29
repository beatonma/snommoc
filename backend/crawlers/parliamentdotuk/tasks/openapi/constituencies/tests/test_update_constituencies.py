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
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        update_constituency_boundaries(context=CONTEXT)

    def test_update_constituency_boundaries(self):
        boundary_json = self.constituency.boundary.geo_json

        match boundary_json:
            case {
                "type": "MultiPolygon",
                "coordinates": list(coordinates),
            }:
                # match first coordinate
                latitude, longitude = coordinates[0][0][0]
                self.assertEqual(latitude, -6.683869292366397)
                self.assertEqual(longitude, 56.97145915072452)

                # match last coordinate
                latitude, longitude = coordinates[-1][-1][-1]
                self.assertEqual(latitude, -4.288692136669457)
                self.assertEqual(longitude, 57.48458249179726)

            case _:
                raise AssertionError(
                    "ConstituencyBoundary.geo_json does not match expected structure",
                    boundary_json,
                )


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

        hendry: ConstituencyCandidate = detail.candidates.get(name="Drew Hendry")
        self.assertEqual(hendry.votes, 15999)
        self.assertEqual(hendry.order, 2)
        self.assertEqual(hendry.party.name, "Scottish National Party")
        self.assertEqual(hendry.result_change, "-15.4%")
