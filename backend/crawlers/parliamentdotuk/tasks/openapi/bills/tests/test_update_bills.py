from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks import update_bills
from crawlers.parliamentdotuk.tasks.openapi.testcase import OpenApiTestCase
from notifications.models import TaskNotification
from repository.models import Bill, BillStageType, BillType
from repository.tests.data.create import create_sample_party

CONTEXT = TaskContext(None, TaskNotification(), follow_pagination=False)


class UpdateBillsTests(OpenApiTestCase):
    file = __file__
    mock_response = {
        "https://bills-api.parliament.uk/api/v1/Bills?SortOrder=DateUpdatedDescending": "data/bills.json",
        "https://bills-api.parliament.uk/api/v1/BillTypes": "data/bill_types.json",
        "https://bills-api.parliament.uk/api/v1/Stages": "data/bill_stages.json",
        "https://bills-api.parliament.uk/api/v1/Bills/2818": "data/bill-2818.json",
        "https://bills-api.parliament.uk/api/v1/Bills/2818/Stages": "data/bill-2818_stages.json",
        "https://bills-api.parliament.uk/api/v1/Bills/512/Publications": "data/bill-2818_publications.json",
    }

    @classmethod
    def setUpTestData(cls):
        create_sample_party("Conservative")
        with cls.patch():
            update_bills(context=CONTEXT)

    def setUp(self):
        self.bill = Bill.objects.get(parliamentdotuk=2818)

    def test_update_bills(self):
        bill = self.bill
        self.assertEqual(bill.title, "Abolition of Business Rates Bill")
        self.assertEqual(
            bill.long_title,
            "A Bill to abolish business rates; and for connected purposes.",
        )
        self.assertEqual(
            bill.bill_type.name, "Private Members' Bill (under the Ten Minute Rule)"
        )
        self.assertFalse(bill.is_act)
        self.assertFalse(bill.is_defeated)

    def test_stage_type_definition_updated(self):
        stage_type = BillStageType.objects.get(parliamentdotuk=38)
        self.assertEqual(stage_type.name, "Legislative Grand Committee")
        self.assertEqual(stage_type.house.name, "Commons")

    def test_bill_type_definitions_updated(self):
        bill_type = BillType.objects.get(parliamentdotuk=2)
        self.assertEqual(bill_type.category.name, "Public")
        self.assertEqual(
            bill_type.name, "Private Members' Bill (Starting in the House of Lords)"
        )
        self.assertEqual(
            bill_type.description,
            "Private Members' bills in the Lords are usually introduced through a ballot"
            " held on the day after State Opening of a new session of a parliament. In order to"
            " enter the ballot, Peers must submit a draft of their bill (including its short and"
            " long title, and all clauses and schedules) to the Legislation Office.<br>"
            '<a href="https://www.parliament.uk/about/how/laws/bills/private-members/" '
            'rel="noopener noreferrer">Find out more about Private Members\' Bills in the Lords</a>',
        )

    def test_bill_sponsors(self):
        sponsor = self.bill.sponsors.first().member
        self.assertEqual(sponsor.name, "Kevin Hollinrake")
        self.assertEqual(sponsor.party.name, "Conservative")

    def test_bill_stages(self):
        current_stage = self.bill.current_stage()
        self.assertEqual(current_stage.description, "2nd reading")
        self.assertEqual(current_stage.house.name, "Commons")

    def test_bill_agent(self):
        agent = self.bill.agent
        self.assertEqual(agent.name, "Agent name")
        self.assertEqual(agent.address, "Agent address")
        self.assertEqual(str(agent.phone_number), "01632 960001")
        self.assertEqual(agent.email, "agent@example.com")
        self.assertEqual(agent.website, "https://agent.example.com")

    def test_bill_promoters(self):
        promoter = self.bill.promoters.first()
        self.assertEqual(promoter.name, "Promoter")
        self.assertEqual(promoter.url, "https://promoter.example.com")
