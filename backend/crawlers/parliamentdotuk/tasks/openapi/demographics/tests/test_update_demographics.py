from datetime import date

from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks.openapi.demographics.update import (
    update_demographics,
)
from crawlers.parliamentdotuk.tasks.openapi.testcase import OpenApiTestCase
from notifications.models import TaskNotification
from repository.models import Party

CONTEXT = TaskContext(None, TaskNotification())


class UpdateDemographicsTests(OpenApiTestCase):
    file = __file__
    mock_response = {
        "https://members-api.parliament.uk/api/Parties/StateOfTheParties/1/2024-11-28": "data/state_of_parties_commons.json",
        "https://members-api.parliament.uk/api/Parties/StateOfTheParties/2/2024-11-28": "data/state_of_parties_lords.json",
        "https://members-api.parliament.uk/api/Parties/LordsByType/2024-11-28": "data/lords_by_type.json",
    }

    @classmethod
    def setUpTestData(cls):
        update_demographics(
            context=CONTEXT,
            for_date=date(2024, 11, 28),
        )

    def test_party_demographics(self):
        labour, _ = Party.objects.resolve(name="Labour")
        labour_commons = labour.gender_demographics.get(house__name="Commons")

        self.assertEqual(labour_commons.male_member_count, 216)
        self.assertEqual(labour_commons.female_member_count, 186)
        self.assertEqual(labour_commons.non_binary_member_count, 0)
        self.assertEqual(labour_commons.total_member_count, 402)

        bishops, _ = Party.objects.resolve(name="Bishops")
        bishops_lords = bishops.gender_demographics.get(house__name="Lords")
        self.assertEqual(bishops_lords.male_member_count, 18)
        self.assertEqual(bishops_lords.female_member_count, 7)
        self.assertEqual(bishops_lords.non_binary_member_count, 0)
        self.assertEqual(bishops_lords.total_member_count, 25)

    def test_lords_demographics(self):
        crossbench, _ = Party.objects.resolve(name="Crossbench")
        lords_crossbench = crossbench.lords_demographics

        self.assertEqual(lords_crossbench.life_count, 151)
        self.assertEqual(lords_crossbench.hereditary_count, 33)
        self.assertEqual(lords_crossbench.bishop_count, 0)
        self.assertEqual(lords_crossbench.total_count, 184)
