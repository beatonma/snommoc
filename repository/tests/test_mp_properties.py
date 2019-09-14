from repository.models import (
    Mp,
    Party,
    Constituency,
)
from repository.models.contact_details import PersonalLinks
from repository.tests import values
from repository.tests.base import BaseRepositoryLocalTestCase


class MpPropertiesTest(BaseRepositoryLocalTestCase):
    def setUp(self) -> None:
        self.mp = Mp.create(
            name=values.EXAMPLE_NAME,
            puk=values.EXAMPLE_PUK_ID,
            twfy=values.EXAMPLE_TWFY_ID)

    def test_set_party(self):
        self.mp.party = Party.objects.create(
            name=values.PARTY_NAME,
            long_name=values.PARTY_NAME_LONG,
            short_name=values.PARTY_NAME_SHORT)
        self.assertEqual(self.mp.party.name, values.PARTY_NAME)

    def test_set_constituency(self):
        constituency = Constituency.objects.create(
            name=values.CONSTITUENCY,
            mp=self.mp)
        constituency.save()

        self.assertEqual(
            self.mp.constituency.name,
            values.CONSTITUENCY)

    def tearDown(self) -> None:
        self.delete_instances_of(Mp, Constituency)


class CompleteMpPropertiesTest(BaseRepositoryLocalTestCase):
    def setUp(self) -> None:
        Party.objects.create(
            name=values.PARTY_NAME,
            short_name=values.PARTY_NAME_SHORT,
            long_name=values.PARTY_NAME_LONG).save()

        Constituency.objects.create(name=values.CONSTITUENCY).save()

        self.mp = Mp.create(
            name=values.EXAMPLE_NAME,
            aliases=values.EXAMPLE_ALIASES,
            puk=values.EXAMPLE_PUK_ID,
            twfy=values.EXAMPLE_TWFY_ID,
            party=values.PARTY_NAME,
            constituency=values.CONSTITUENCY,
            phone_constituency=values.PHONE_CONSTITUENCY,
            phone_parliamentary=values.PHONE_PARLIAMENT,
            email=values.EMAIL,
            interests_countries=values.INTEREST_COUNTRY,
            interests_political=values.INTEREST_POLITICAL,
            weblinks=values.WEBLINKS,
            wikipedia_path=values.WIKIPEDIA
        )

    def test_mp_interests_properties(self):
        self.assertListEqual(
            self.mp.political_interests,
            values.INTEREST_POLITICAL)
        self.assertListEqual(
            self.mp.countries_of_interest,
            values.INTEREST_COUNTRY)

    def test_mp_to_json(self):
        json_data = self.mp.to_json()
        self.assertEqual(json_data, values.MP_STRUCTURE)

    def tearDown(self) -> None:
        self.delete_instances_of(PersonalLinks, Mp, Party, Constituency)
