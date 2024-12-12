from basetest.testcase import DatabaseTestCase
from repository.models import Constituency
from repository.tests.data.create import create_sample_constituency


class PartyQuerySetTests(DatabaseTestCase):
    def test_search(self):
        ynys = create_sample_constituency("Ynys Môn")
        self.assertEqual(Constituency.objects.search("mon").first(), ynys)
