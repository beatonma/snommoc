from datetime import date

from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks import update_lords_divisions
from crawlers.parliamentdotuk.tasks.openapi.testcase import OpenApiTestCase
from notifications.models import TaskNotification
from repository.models import LordsDivision
from repository.tests.data.create import create_sample_party

CONTEXT = TaskContext(None, TaskNotification(), max_items=1)


class UpdateLordsDivisionsTests(OpenApiTestCase):
    file = __file__
    mock_response = {
        "https://lordsvotes-api.parliament.uk/data/Divisions/search": "data/lords.json",
    }

    @classmethod
    def setUpTestData(cls):
        create_sample_party(name="Conservative")
        update_lords_divisions(context=CONTEXT)

    def test_update_lords_divisions(self):
        division = LordsDivision.objects.get(parliamentdotuk=3172)
        self.assertEqual(division.date, date(2024, 11, 20))
        self.assertEqual(division.number, 5)
        self.assertEqual(division.title, "Water (Special Measures) Bill [HL]")
        self.assertFalse(division.is_whipped)
        self.assertFalse(division.is_government_content)
        self.assertEqual(division.ayes, 36)
        self.assertEqual(division.noes, 89)
        self.assertEqual(
            division.amendment_motion_notes,
            "<p>Lord Roborough moved amendment 51, to leave out clause 10. The House divided:</p>",
        )

        self.assertQuerysetSize(division.votes.filter(vote_type__name="content"), 36)
        self.assertQuerysetSize(
            division.votes.filter(vote_type__name="not_content"), 89
        )
        self.assertQuerysetSize(division.votes.filter(is_teller=True), 4)

        aye = division.votes.get(person__parliamentdotuk=36)
        self.assertEqual(aye.vote_type.name, "content")
        self.assertEqual(aye.person.name, "Baroness Laing of Elderslie")
        self.assertEqual(aye.person.party.name, "Conservative")
