from basetest.testcase import LocalTestCase
from repository.models import Party, PartyAlsoKnownAs
from repository.resolution.party import get_party_by_name
from repository.tests.data.create import create_sample_parties


class PartyResolutionTest(LocalTestCase):
    def setUp(self) -> None:
        create_sample_parties()

    def test_get_party_by_name(self):
        self.assertEqual(get_party_by_name("Labour").pk, 15)
        self.assertEqual(get_party_by_name("Conservative").pk, 4)

        self.assertEqual(get_party_by_name("labour").pk, 15)

    def test_get_party_by_name__alias(self):
        PartyAlsoKnownAs.objects.create(
            canonical=get_party_by_name("Labour"),
            alias="Labour UK",
        )

        PartyAlsoKnownAs.objects.create(
            canonical=get_party_by_name("conservative"),
            alias="Conservative & Unionist Party",
        )

        self.assertEqual(get_party_by_name("labour uk").pk, 15)
        self.assertEqual(get_party_by_name("Conservative & Unionist Party").pk, 4)

    def tearDown(self) -> None:
        self.delete_instances_of(
            Party,
            PartyAlsoKnownAs,
        )
