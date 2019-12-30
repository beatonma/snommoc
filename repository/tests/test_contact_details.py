from api import contract as api_contract
from repository.models import Mp
from repository.models.contact_details import Links
from repository.models.person import Person
from repository.tests import values
from repository.tests.base import BaseRepositoryLocalTestCase


class ContactDetailsTest(BaseRepositoryLocalTestCase):
    """"""
    def setUp(self) -> None:
        self.person = Person.objects.create(name=values.EXAMPLE_NAME)
        # self.mp = Mp.create(name=values.EXAMPLE_NAME, puk=values.EXAMPLE_PUK_ID)

    def test_linksdotcreate(self):
        links = Links.create(
            person=self.person,
            email=values.EMAIL,
            phone_parliament=values.PHONE_PARLIAMENT,
            phone_constituency=values.PHONE_CONSTITUENCY,
            weblinks=values.WEBLINKS,
            wikipedia=values.WIKIPEDIA)

        self.assertEqual(len(links.weblinks.all()), 1)
        self.assertEqual(links.weblinks.first().url, values.WEBLINKS[0])
        self.assertEqual(links.email, values.EMAIL)
        self.assertEqual(links.wikipedia, values.WIKIPEDIA)
        self.assertEqual(links.phone_constituency, '+443069990924')
        self.assertEqual(links.phone_parliament, '+442079460513')

    def test_links_dot_create_with_no_data_should_be_none(self):
        links = Links.create(person=self.person)
        self.assertIsNone(links)

    def test_mpreverserelation(self):
        links = Links.create(
            person=self.person,
            email=values.EMAIL,
            phone_parliament=values.PHONE_PARLIAMENT,
            phone_constituency=values.PHONE_CONSTITUENCY,
            weblinks=values.WEBLINKS,
            wikipedia=values.WIKIPEDIA)

        self.assertEqual(self.person.links, links)

    # def test_links_to_json(self):
    #     links = Links.create(
    #         person=self.person,
    #         email=values.EMAIL,
    #         phone_parliament=values.PHONE_PARLIAMENT,
    #         phone_constituency=values.PHONE_CONSTITUENCY,
    #         weblinks=values.WEBLINKS,
    #         wikipedia=values.WIKIPEDIA)
    #
    #     json = links.to_json()
    #     self.assertEqual(json.get(api_contract.EMAIL), values.EMAIL)
    #     self.assertListEqual(json.get(api_contract.WEBLINKS), values.WEBLINKS)

    def tearDown(self) -> None:
        self.delete_instances_of(Links, Mp)
