import datetime

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda.bills import (
    _update_bill,
    _update_bill_publication,
    _update_bill_stage,
    _update_sponsor,
)
from crawlers.parliamentdotuk.tests.lda.data_lda_update_bills import (
    EXAMPLE_BILL,
    EXAMPLE_BILL_PUBLICATION,
    EXAMPLE_BILL_SPONSOR,
    EXAMPLE_BILL_STAGE,
)
from repository.models import (
    Bill,
    BillPublication,
    BillSponsor,
    BillStageSitting,
    BillStageType,
    ParliamentarySession,
    Person,
)


class UpdateBillPartialTests(LocalTestCase):
    """"""

    def setUp(self) -> None:
        Bill.objects.create(
            parliamentdotuk=754405,
            title="title",
            description="description",
            date=datetime.date(2018, 12, 21),
            act_name="act_name",
            label="label",
            homepage="https://homepage.example.org",
        )

    def _get_bill(self):
        return Bill.objects.get(parliamentdotuk=754405)

    def test_update_bill_stage(self):
        data = EXAMPLE_BILL_STAGE
        bill = self._get_bill()

        _update_bill_stage(bill, data)

        sittings = BillStageSitting.objects.all()
        self.assertLengthEquals(sittings, 1)

        sitting: BillStageSitting = sittings.first()
        self.assertEqual(sitting.parliamentdotuk, 12546)
        self.assertEqual(sitting.date, datetime.date(year=2018, month=5, day=9))
        self.assertFalse(sitting.formal)
        self.assertFalse(sitting.provisional)

        sessions = ParliamentarySession.objects.all()
        self.assertLengthEquals(sessions, 1)

        session: ParliamentarySession = sessions.first()
        self.assertEqual(session.parliamentdotuk, 730830)
        self.assertEqual(session.name, "2017-2019")

        stage_types = BillStageType.objects.all()
        self.assertLengthEquals(stage_types, 1)

        stage_type: BillStageType = stage_types.first()
        self.assertEqual(stage_type.parliamentdotuk, 392164)
        self.assertEqual(stage_type.name, "Committee stage")

    def test_update_bill_publication(self):
        data = EXAMPLE_BILL_PUBLICATION
        bill = self._get_bill()

        _update_bill_publication(bill, data)

        publication = BillPublication.objects.get(pk=1030167)
        self.assertEqual(
            publication.title,
            "Prisons (Interference with Wireless Telegraphy) Act 2018 (c. 32)",
        )

    def test_update_bill_sponsors__no_person(self):
        """A Person instance matching sponsor name cannot be found."""

        data = EXAMPLE_BILL_SPONSOR
        bill = self._get_bill()

        _update_sponsor(bill, data)

        nameonly_sponsor: BillSponsor = BillSponsor.objects.first()
        self.assertIsNone(nameonly_sponsor.person)
        self.assertEqual(nameonly_sponsor.name, "Baroness Pidding")
        self.assertEqual(nameonly_sponsor.bill, bill)

    def test_update_bill_sponsors(self):
        """A Person instance is found for the sponsor name."""
        data = EXAMPLE_BILL_SPONSOR
        bill = self._get_bill()
        Person.objects.create(
            parliamentdotuk=12345,
            name="Baroness Pidding",
            active=True,
            house_id=0,
        )

        _update_sponsor(bill, data)

        nameonly_sponsor: BillSponsor = BillSponsor.objects.first()
        self.assertEqual(nameonly_sponsor.name, "Baroness Pidding")
        self.assertEqual(nameonly_sponsor.person.name, "Baroness Pidding")
        self.assertEqual(nameonly_sponsor.bill, bill)

    def tearDown(self) -> None:
        self.delete_instances_of(
            Bill,
            BillPublication,
            BillStageSitting,
            ParliamentarySession,
            BillStageType,
            Person,
        )


class UpdateBillTests(LocalTestCase):
    """"""

    def test_update_bill(self):
        data = EXAMPLE_BILL
        _update_bill(754405, data)

        bill = Bill.objects.first()
        self.assertEqual(bill.parliamentdotuk, 754405)
        self.assertEqual(bill.bill_chapter, "32")
        self.assertEqual(bill.ballot_number, 13)
        self.assertEqual(
            bill.act_name, "Prisons (Interference with Wireless Telegraphy) Act 2018"
        )
        self.assertEqual(
            bill.title, "Prisons (Interference with Wireless Telegraphy) Bill"
        )
        self.assertEqual(
            bill.description,
            "A Bill to make provision about interference with wireless telegraphy in prisons and similar institutions.",
        )
        self.assertEqual(bill.label, "Prisons (Interference with Wireless Telegraphy)")
        self.assertEqual(bill.date, datetime.date(year=2018, month=12, day=21))
        self.assertEqual(
            bill.homepage,
            "http://services.parliament.uk/bills/2017-19/prisonsinterferencewithwirelesstelegraphy.html",
        )

        self.assertFalse(bill.is_money_bill)
        self.assertFalse(bill.is_private)
        self.assertFalse(bill.public_involvement_allowed)

        self.assertLengthEquals(bill.sponsors.all(), 2)
        self.assertLengthEquals(bill.stages.all(), 11)
        self.assertLengthEquals(bill.publications.all(), 12)

        self.assertEqual(bill.bill_type.name, "Ballot")
        self.assertEqual(
            bill.bill_type.description, "Private Members' Bill (Ballot Bill)"
        )
