import datetime

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.openapi.bills.billstagetypes import (
    _update_bill_stage_type,
)
from crawlers.parliamentdotuk.tasks.openapi.bills.billtypes import _update_bill_type
from crawlers.parliamentdotuk.tasks.openapi.bills.update import (
    _update_bill,
)
from crawlers.parliamentdotuk.tests.openapi.data_bill import (
    BILL_DATA,
    BILL_STAGE_DATA,
    BILL_TYPE_DATA,
)
from notifications.models import TaskNotification
from repository.models import Organisation, ParliamentarySession
from repository.models.bill import (
    Bill,
    BillAgent,
    BillSponsor,
    BillStage,
    BillStageSitting,
    BillStageType,
    BillType,
    BillTypeCategory,
)
from repository.tests.data.create import (
    create_sample_bill_stage_type,
    create_sample_bill_type,
    create_sample_person,
    create_sample_session,
)


class BillUpdateTests(LocalTestCase):
    def test_update_bill_type(self):
        _update_bill_type(BILL_TYPE_DATA, notification=None)

        billtype = BillType.objects.get(parliamentdotuk=4)
        self.assertEqual(billtype.category.name, "Hybrid")
        self.assertEqual(billtype.name, "Hybrid Bill")
        self.assertTrue(
            billtype.description.startswith("Hybrid Bills mix the characteristics")
        )

    def test_update_bill_stage_type(self):
        _update_bill_stage_type(BILL_STAGE_DATA, notification=None)

        stage = BillStageType.objects.get(parliamentdotuk=42)
        self.assertEqual(stage.name, "Consideration of Lords message")
        self.assertEqual(stage.house.name, "Commons")

    def test_update_bill(self):
        create_sample_session(parliamentdotuk=24, name="Sample session")
        create_sample_bill_type(parliamentdotuk=4)
        create_sample_bill_stage_type(parliamentdotuk=11)
        create_sample_person(parliamentdotuk=1414, name="Mr Mark Hoban")

        _update_bill(BILL_DATA, notification=None)

        bill = Bill.objects.get(pk=836)

        self.assertEqual(bill.short_title, "Appropriation Act 2011")
        self.assertTrue(bill.long_title.startswith("A Bill To authorise "))
        self.assertTrue(bill.summary.startswith("<p>The Bill provides "))
        self.assertEqual(bill.current_house.name, "Unassigned")
        self.assertEqual(bill.originating_house.name, "Commons")
        self.assertDateTimeEqual(
            bill.last_update,
            datetime.datetime(2012, 3, 28, 9, 58, 29),
        )
        self.assertIsNone(bill.bill_withdrawn)
        self.assertFalse(bill.is_defeated)
        self.assertTrue(bill.is_act)

        self.assertEqual(bill.bill_type.pk, 4)
        self.assertEqual(bill.introduced_session_id, 24)
        self.assertEqual(bill.included_sessions.first().pk, 24)

        sponsors = bill.sponsors.all()
        self.assertLengthEquals(sponsors, 2)
        sponsor = sponsors.get(member_id=1414)
        self.assertEqual(sponsor.member.name, "Mr Mark Hoban")
        self.assertEqual(sponsor.organisation.name, "HM Treasury")

        promoter = bill.promoters.first()
        self.assertEqual(promoter.name, "Sample promoter")
        self.assertEqual(promoter.url, "https://snommoc.org/promoter")

        agent = bill.agent
        self.assertEqual(agent.name, "Sample agent")
        self.assertEqual(agent.address, "Sample address")
        self.assertEqual(agent.phone_number, "01234 567890")
        self.assertEqual(agent.email, "sample@snommoc.org")
        self.assertEqual(agent.website, "https://snommoc.org")

    def tearDown(self) -> None:
        self.delete_instances_of(
            Bill,
            BillAgent,
            BillSponsor,
            BillStage,
            BillStageType,
            BillStageSitting,
            BillType,
            BillTypeCategory,
            Organisation,
            ParliamentarySession,
            TaskNotification,
        )
