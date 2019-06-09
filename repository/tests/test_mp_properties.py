from api import contract as api_contract
from basetest.testcase import LocalTestCase
from repository.models import (
    Mp,
    Party,
    Constituency,
    NameAlias,
)
from repository.tests import constants
from repository.tests.constants import EXAMPLE_ALIASES


class MpPropertiesTest(LocalTestCase):
    """"""

    def setUp(self) -> None:
        self.mp = Mp.create(
            name=constants.EXAMPLE_NAME,
            puk=constants.EXAMPLE_PUK_ID,
            twfy=constants.EXAMPLE_TWFY_ID)

    def test_set_party(self):
        self.mp.party = Party.objects.create(
            name=constants.PARTY_NAME,
            long_name=constants.PARTY_NAME_LONG,
            short_name=constants.PARTY_NAME_SHORT)
        self.assertEqual(self.mp.party.name, constants.PARTY_NAME)

    def test_set_constituency(self):
        constituency = Constituency.objects.create(
            name=constants.CONSTITUENCY,
            mp=self.mp)
        constituency.save()

        self.assertEqual(
            self.mp.constituency.name,
            constants.CONSTITUENCY)


class CompleteMpPropertiesTest(LocalTestCase):
    def setUp(self) -> None:
        Party.objects.create(
            name=constants.PARTY_NAME,
            short_name=constants.PARTY_NAME_SHORT,
            long_name=constants.PARTY_NAME_LONG).save()

        Constituency.objects.create(name=constants.CONSTITUENCY).save()

        self.mp = Mp.create(
            name=constants.EXAMPLE_NAME,
            puk=constants.EXAMPLE_PUK_ID,
            twfy=constants.EXAMPLE_TWFY_ID,
            party=constants.PARTY_NAME,
            constituency=constants.CONSTITUENCY,
            phone_constituency=constants.PHONE_CONSTITUENCY,
            phone_parliamentary=constants.PHONE_PARLIAMENT,
            email=constants.EMAIL,
            interests_countries=constants.INTEREST_COUNTRY,
            interests_political=constants.INTEREST_POLITICAL,
            weblinks=constants.WEBLINKS,
            wikipedia_path=constants.WIKIPEDIA
        )

        for alias in EXAMPLE_ALIASES:
            NameAlias.objects.create(person=self.mp, name=alias).save()

    def test_mp_interests_properties(self):
        self.assertListEqual(
            self.mp.political_interests,
            constants.INTEREST_POLITICAL)
        self.assertListEqual(
            self.mp.countries_of_interest,
            constants.INTEREST_COUNTRY)

    def test_mp_to_json(self):
        json = self.mp.to_json()
        self.assertEqual(json[api_contract.NAME], constants.EXAMPLE_NAME)
        self.assertEqual(json[api_contract.ALIASES], constants.EXAMPLE_ALIASES)
        self.assertEqual(json[api_contract.THEYWORKFORYOU_ID], constants.EXAMPLE_TWFY_ID)
        self.assertEqual(json[api_contract.PARLIAMENTDOTUK_ID], constants.EXAMPLE_PUK_ID)
        self.assertEqual(json[api_contract.PARTY], constants.PARTY_NAME)
        self.assertEqual(json[api_contract.CONSTITUENCY], constants.CONSTITUENCY)

        interests = json[api_contract.INTERESTS]
        self.assertListEqual(interests[api_contract.INTERESTS_POLITICAL],
                             constants.INTEREST_POLITICAL)
        self.assertListEqual(interests[api_contract.INTERESTS_COUNTRIES],
                             constants.INTEREST_COUNTRY)

        links = json[api_contract.PERSONAL_LINKS]
        self.assertEqual(links[api_contract.EMAIL], constants.EMAIL)
        self.assertListEqual(links[api_contract.WEBLINKS], constants.WEBLINKS)
        self.assertEqual(links[api_contract.WIKIPEDIA], constants.WIKIPEDIA)

        phone = links[api_contract.PHONE]
        self.assertEqual(phone[api_contract.PHONE_PARLIAMENT].replace(' ', ''),
                         constants.PHONE_PARLIAMENT)
        self.assertEqual(phone[api_contract.PHONE_CONSTITUENCY].replace(' ', ''),
                         constants.PHONE_CONSTITUENCY)
