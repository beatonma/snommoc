from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.openapi.bills.billpublications import (
    _update_bill_publication,
)
from crawlers.parliamentdotuk.tasks.openapi.bills.billstages import _update_bill_stage
from crawlers.parliamentdotuk.tasks.openapi.bills.billstagetypes import (
    _update_bill_stage_type,
)
from crawlers.parliamentdotuk.tasks.openapi.bills.billtypes import _update_bill_type
from crawlers.parliamentdotuk.tasks.openapi.bills.update import update_bill
from crawlers.parliamentdotuk.tests.openapi.data_bill import (
    BILL_DATA,
    BILL_PUBLICATION_DATA,
    BILL_STAGE_DATA,
    BILL_STAGE_TYPE_DATA,
    BILL_TYPE_DATA,
)
from notifications.models import TaskNotification
from repository.models import House, Organisation, ParliamentarySession, Person
from repository.models.bill import (
    Bill,
    BillAgent,
    BillPublication,
    BillPublicationLink,
    BillPublicationType,
    BillSponsor,
    BillStage,
    BillStageSitting,
    BillStageType,
    BillType,
    BillTypeCategory,
)
from repository.tests.data.create import (
    create_sample_bill,
    create_sample_bill_stage_type,
    create_sample_bill_type,
    create_sample_person,
    create_sample_session,
)
from util.time import tzdatetime


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
        _update_bill_stage_type(BILL_STAGE_TYPE_DATA, notification=None)

        stage = BillStageType.objects.get(parliamentdotuk=42)
        self.assertEqual(stage.name, "Consideration of Lords message")
        self.assertEqual(stage.house.name, "Commons")

    def test_update_bill(self):
        create_sample_session(parliamentdotuk=24, name="Sample session")
        create_sample_bill_type(parliamentdotuk=4)
        create_sample_bill_stage_type(parliamentdotuk=11)
        create_sample_person(parliamentdotuk=1414, name="Mr Mark Hoban")

        update_bill(BILL_DATA, notification=None)

        bill = Bill.objects.get(pk=836)

        self.assertEqual(bill.title, "Appropriation Act 2011")
        self.assertTrue(bill.long_title.startswith("A Bill To authorise "))
        self.assertTrue(bill.summary.startswith("<p>The Bill provides "))
        self.assertEqual(bill.current_house.name, "Unassigned")
        self.assertEqual(bill.originating_house.name, "Commons")
        self.assertEqual(
            bill.last_update,
            tzdatetime(2012, 3, 28, 9, 58, 29),
        )
        self.assertIsNone(bill.withdrawn_at)
        self.assertFalse(bill.is_defeated)
        self.assertTrue(bill.is_act)

        self.assertEqual(bill.bill_type.pk, 4)
        self.assertEqual(bill.session_introduced_id, 24)
        self.assertEqual(bill.sessions.first().pk, 24)

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

    def test_update_bill_stages(self):
        create_sample_session(parliamentdotuk=24, name="Sample session")
        create_sample_bill_stage_type(parliamentdotuk=6)

        _update_bill_stage(BILL_STAGE_DATA, None, {"bill_id": 836})

        stage = BillStage.objects.first()
        self.assertEqual(stage.pk, 4116)
        self.assertEqual(stage.bill_id, 836)
        self.assertEqual(stage.description, "1st reading")
        self.assertEqual(stage.abbreviation, "1R")
        self.assertEqual(stage.house.name, "Commons")
        self.assertEqual(stage.stage_type_id, 6)
        self.assertEqual(stage.session_id, 24)
        self.assertEqual(stage.sort_order, 1)

        sitting = stage.sittings.first()
        self.assertEqual(sitting.pk, 3879)
        self.assertEqual(sitting.date, tzdatetime(2011, 3, 2, 0, 0, 0))

    def test_update_bill_publication(self):
        create_sample_bill(parliamentdotuk=723)

        _update_bill_publication(
            BILL_PUBLICATION_DATA, notification=None, func_kwargs={"bill_id": 723}
        )

        pub = BillPublication.objects.first()
        self.assertEqual(pub.house.name, "Commons")
        self.assertEqual(pub.parliamentdotuk, 2716)
        self.assertTrue(pub.title.startswith("Public Administration "))
        self.assertEqual(pub.display_date, tzdatetime(2008, 6, 4))

        pub_type = pub.publication_type
        self.assertEqual(pub_type.parliamentdotuk, 9)
        self.assertEqual(pub_type.name, "Select Committee report")
        self.assertTrue(pub_type.description.startswith("The following select "))

        link = pub.links.first()
        self.assertEqual(link.parliamentdotuk, 3096)
        self.assertEqual(link.content_type, "text/html")
        self.assertTrue(link.title.startswith("Public Admin"))
        self.assertTrue(link.url.startswith("https://www.publ"))

    def tearDown(self) -> None:
        self.delete_instances_of(
            Bill,
            BillAgent,
            BillPublication,
            BillPublicationLink,
            BillPublicationType,
            BillSponsor,
            BillStage,
            BillStageType,
            BillStageSitting,
            BillType,
            BillTypeCategory,
            House,
            Organisation,
            ParliamentarySession,
            Person,
            TaskNotification,
        )
