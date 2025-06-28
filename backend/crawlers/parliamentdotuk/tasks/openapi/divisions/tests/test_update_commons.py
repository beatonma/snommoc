from datetime import date

from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks.openapi.divisions.commons import (
    update_commons_divisions,
)
from crawlers.parliamentdotuk.tasks.openapi.testcase import OpenApiTestCase
from notifications.models import TaskNotification
from repository.models import CommonsDivision
from repository.tests.data.create import create_sample_party

CONTEXT = TaskContext(None, TaskNotification(), max_items=1)


class UpdateCommonsDivisionsTests(OpenApiTestCase):
    file = __file__
    mock_response = {
        "https://commonsvotes-api.parliament.uk/data/divisions.json/search": "data/commons.json",
        "https://commonsvotes-api.parliament.uk/data/division/1873.json": "data/commons-1873.json",
    }

    @classmethod
    def setUpTestData(cls):
        create_sample_party(name="Labour")
        update_commons_divisions(context=CONTEXT)

    def test_update_commons_divisions(self):
        division = CommonsDivision.objects.get(parliamentdotuk=1873)
        self.assertEqual(
            division.title,
            "Non-Domestic Rating (Multipliers and Private Schools) Bill: Second Reading",
        )
        self.assertEqual(division.date, date(2024, 11, 25))
        self.assertEqual(division.number, 47)
        self.assertEqual(division.ayes, 336)
        self.assertEqual(division.noes, 175)
        self.assertEqual(division.did_not_vote, 139)
        self.assertTrue(division.is_passed)
        self.assertFalse(division.is_deferred_vote)

        # Numbers do not match totals described above but match source data
        self.assertQuerysetSize(division.votes.filter(vote_type__name="aye"), 335)
        self.assertQuerysetSize(division.votes.filter(vote_type__name="no"), 176)
        self.assertQuerysetSize(
            division.votes.filter(vote_type__name="did_not_vote"), 139
        )
        self.assertQuerysetSize(division.votes.filter(is_teller=True), 4)

        aye = division.votes.get(person__parliamentdotuk=5104)
        self.assertEqual(aye.vote_type.name, "aye")
        self.assertEqual(aye.person.name, "Gill German")
        self.assertEqual(aye.person.party.name, "Labour")
