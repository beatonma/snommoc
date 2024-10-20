from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.openapi.bills.schema import (
    Bill,
    BillPublication,
    BillStageType,
    BillSummary,
    House,
)
from crawlers.parliamentdotuk.tasks.openapi.divisions.schema import LordsDivision
from crawlers.parliamentdotuk.tests.openapi.data_bill import (
    BILL_DATA,
    BILL_PUBLICATION_DATA,
    BILL_STAGE_TYPE_DATA,
    BILL_SUMMARY_DATA,
)
from crawlers.parliamentdotuk.tests.openapi.data_lordsdivision import (
    LORDS_DIVISION_DATA,
)
from util.time import tzdatetime


class ApiViewmodelTestCase(LocalTestCase):
    """Ensure data from the API constructs our models correctly."""

    def test_lordsdivision_schemas(self):
        division = LordsDivision(**LORDS_DIVISION_DATA)

        self.assertEqual(2613, division.divisionId)
        self.assertEqual(3, len(division.contents))
        self.assertEqual("Lord Pendry", division.contents[0].name)

    def test_billsummary_schemas(self):
        bill = BillSummary(**BILL_SUMMARY_DATA)

        self.assertEqual(bill.billId, 512)
        self.assertEqual(bill.introducedSessionId, 22)
        self.assertEqual(bill.currentHouse, House.Unassigned)
        self.assertEqual(bill.originatingHouse, House.Commons)
        self.assertEqual(bill.includedSessionIds, [22, 23])

        stage = bill.currentStage
        self.assertEqual(len(stage.stageSittings), 1)
        sitting = stage.stageSittings[0]

        self.assertEqual(stage.description, "Royal Assent")
        self.assertEqual(stage.house, House.Unassigned)

        self.assertEqual(sitting.date, tzdatetime(2010, 4, 8))

    def test_bill_schemas(self):
        bill = Bill(**BILL_DATA)

        self.assertEqual(
            bill.longTitle,
            "A Bill To authorise the use of resources for the service of the years"
            " ending with 31 March 2010 and 31 March 2011 and to apply certain sums out"
            " of the Consolidated Fund to the service of the years ending with 31 March"
            " 2010 and 31 March 2011; and to appropriate the supply authorised in this"
            " Session of Parliament for the service of the years ending with 31 March"
            " 2010 and 31 March 2011.",
        )
        self.assertEqual(
            bill.summary,
            "<p>The Bill provides Parliamentary authority for funds requested by the"
            " Government. It is part of 'supply procedure', which is how Parliament"
            " grants the Government&rsquo;s requests for resources.</p><p>Two"
            " Consolidated Fund (Appropriation) Bills are passed each year, in March"
            " and July. They are sometimes referred to simply as &ldquo;Appropriation"
            " Bills&rdquo;. These, together with the Consolidated Fund Bill, provide"
            " authorisation from Parliament for the resources sought by the Government."
            " Proceedings on the Bill are formal, ie there is no debate and the Bill"
            " goes through 'on the nod'.</p><p><strong>Key"
            " areas</strong></p><ul><li>authorises provision sought in the Spring"
            " Supplementary Estimates for 2010/11 and the Statement of Excesses for"
            " 2009/10</li><li>authorises the release of money from the Consolidated"
            " Fund, which is the Government&rsquo;s bank account</li><li>places limits"
            " on the purposes for which the money may be spent.</li></ul>",
        )

        sponsors = bill.sponsors

        self.assertEqual(len(sponsors), 2)

        sponsor = sponsors[0]
        member = sponsor.member
        org = sponsor.organisation

        self.assertEqual(member.memberId, 1414)
        self.assertEqual(member.name, "Mr Mark Hoban")
        self.assertEqual(member.party, "Conservative")
        self.assertEqual(member.partyColor, "0000ff")
        self.assertEqual(member.house, House.Commons)
        self.assertEqual(
            member.memberPhoto,
            "https://members-api.parliament.uk/api/Members/1414/Thumbnail",
        )
        self.assertEqual(
            member.memberPage, "https://members.parliament.uk/member/1414/contact"
        )
        self.assertEqual(member.memberFrom, "Fareham")

        self.assertEqual(org.name, "HM Treasury")
        self.assertEqual(
            org.url, "https://www.gov.uk/government/organisations/hm-treasury"
        )

        promoter = bill.promoters[0]

        self.assertEqual(promoter.organisationName, "Sample promoter")
        self.assertEqual(promoter.organisationUrl, "https://snommoc.org/promoter")

        self.assertIsNone(bill.petitioningPeriod)
        self.assertIsNone(bill.petitionInformation)
        self.assertEqual(bill.billId, 836)
        self.assertEqual(bill.shortTitle, "Appropriation Act 2011")
        self.assertEqual(bill.currentHouse, House.Unassigned)
        self.assertEqual(bill.originatingHouse, House.Commons)
        self.assertEqual(bill.lastUpdate, tzdatetime(2012, 3, 28, 9, 58, 29))
        self.assertIsNone(bill.billWithdrawn)
        self.assertFalse(bill.isDefeated)
        self.assertEqual(bill.billTypeId, 4)
        self.assertEqual(bill.introducedSessionId, 24)
        self.assertEqual(bill.includedSessionIds, [24])
        self.assertTrue(bill.isAct)

        stage = bill.currentStage
        self.assertEqual(stage.id, 4181)
        self.assertEqual(stage.stageId, 11)
        self.assertEqual(stage.sessionId, 24)
        self.assertEqual(stage.description, "Royal Assent")
        self.assertEqual(stage.abbreviation, "RA")
        self.assertEqual(stage.house, House.Unassigned)

        sitting = stage.stageSittings[0]
        self.assertEqual(sitting.id, 3957)
        self.assertEqual(sitting.stageId, 11)
        self.assertEqual(sitting.billStageId, 4181)
        self.assertEqual(sitting.billId, 836)
        self.assertEqual(sitting.date, tzdatetime(2011, 3, 16))

        agent = bill.agent
        self.assertEqual(
            agent.name,
            "Sample agent",
        )
        self.assertEqual(
            agent.address,
            "Sample address",
        )
        self.assertEqual(
            agent.phoneNo,
            "01234 567890",
        )
        self.assertEqual(
            agent.email,
            "sample@snommoc.org",
        )
        self.assertEqual(agent.website, "https://snommoc.org")

    def test_billstage_schemas(self):
        stage = BillStageType(**BILL_STAGE_TYPE_DATA)

        self.assertEqual(stage.id, 42)
        self.assertEqual(stage.name, "Consideration of Lords message")
        self.assertEqual(stage.house, House.Commons)

    def test_billpublication_schemas(self):
        pub = BillPublication(**BILL_PUBLICATION_DATA)

        self.assertEqual(pub.id, 2716)
        self.assertEqual(pub.house, House.Commons)
        self.assertTrue(pub.title.startswith("Public Administration "))
        self.assertEqual(pub.displayDate, tzdatetime(2008, 6, 4))

        pub_type = pub.publicationType
        self.assertEqual(pub_type.id, 9)
        self.assertEqual(pub_type.name, "Select Committee report")
        self.assertTrue(pub_type.description.startswith("The following "))

        link = pub.links[0]
        self.assertEqual(link.id, 3096)
        self.assertTrue(link.title.startswith("Public Administration "))
        self.assertTrue(link.url.startswith("https://www.publications"))
        self.assertEqual(link.contentType, "text/html")
