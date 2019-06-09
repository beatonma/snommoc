from basetest.testcase import LocalTestCase
from repository.models import Mp
from repository.models.contact_details import PersonalLinks
from repository.tests import constants


class ContactDetailsTest(LocalTestCase):
    def setUp(self) -> None:
        self.mp = Mp.create(name=constants.EXAMPLE_NAME)

    def test_linksdotcreate(self):
        links = PersonalLinks.create(
            person=self.mp,
            email=constants.EMAIL,
            phone_parliament=constants.PHONE_PARLIAMENT,
            phone_constituency=constants.PHONE_CONSTITUENCY,
            weblinks=constants.WEBLINKS,
            wikipedia=constants.WIKIPEDIA)

        self.assertEqual(len(links.weblinks.all()), 1)
        self.assertEqual(links.weblinks.first().url, constants.WEBLINKS[0])
        self.assertEqual(links.email, constants.EMAIL)
        self.assertEqual(links.wikipedia, constants.WIKIPEDIA)
        self.assertEqual(links.phone_constituency, '+443069990924')
        self.assertEqual(links.phone_parliament, '+442079460513')

    def test_links_dot_create_with_no_data_should_be_none(self):
        links = PersonalLinks.create(person=self.mp)
        self.assertIsNone(links)
