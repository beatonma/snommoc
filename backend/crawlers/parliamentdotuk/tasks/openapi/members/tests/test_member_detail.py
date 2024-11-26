from datetime import date

from crawlers.context import TaskContext
from crawlers.parliamentdotuk.tasks.openapi.members.member_detail import (
    update_current_members,
)
from crawlers.parliamentdotuk.tasks.openapi.testcase import OpenApiTestCase
from notifications.models import TaskNotification
from repository.models import Person

CONTEXT = TaskContext(None, TaskNotification())


class UpdateMemberDetailTests(OpenApiTestCase):
    file = __file__
    mock_response = {
        "https://members-api.parliament.uk/api/Members/Search": "data/search.json",
        "https://members-api.parliament.uk/api/Members/4514/Biography": "data/biography.json",
        "https://members-api.parliament.uk/api/Members/4514/Contact": "data/contact.json",
        "https://members-api.parliament.uk/api/Members/4514/Experience": "data/experience.json",
        "https://members-api.parliament.uk/api/Members/4514/RegisteredInterests": "data/registered_interests.json",
        "https://members-api.parliament.uk/api/Members/4514/Focus": "data/focus.json",
    }

    def test_update_member_details(self):
        with self.patch():
            update_current_members(context=CONTEXT)

        person = Person.objects.get(parliamentdotuk=4514)
        self.assertEqual(person.name, "Sir Keir Starmer")
        self.assertEqual(person.full_title, "Rt Hon Sir Keir Starmer MP")
        self.assertEqual(person.gender, "M")

        self._test_party(person)
        self._test_posts(person)
        self._test_registered_interests(person)
        self._test_subjects_of_interest(person)
        self._test_experiences(person)
        self._test_contact(person)
        self._test_party_affiliations(person)
        self._test_constituencies(person)
        self._test_house_memberships(person)
        self._test_elections_contested(person)
        self._test_committees(person)

    def _test_party(self, person: Person):
        self.assertEqual(person.party.name, "Labour")
        self.assertEqual(person.party.theme.primary, "#d50000")

    def _test_posts(self, person: Person):
        self.assertListEqual(
            list(person.current_posts()),
            [
                "Prime Minister and First Lord of the Treasury",
                "Leader of the Labour Party",
            ],
        )
        holder = person.posts.get(post__parliamentdotuk=884)
        post = holder.post
        self.assertEqual(holder.start, date(2015, 9, 18))
        self.assertEqual(holder.end, date(2016, 6, 27))
        self.assertEqual(post.type, "opposition")
        self.assertEqual(post.name, "Shadow Minister (Home Office)")
        self.assertEqual(post.additional_info, "Home Office")
        self.assertEqual(
            post.additional_info_link,
            "https://www.gov.uk/government/organisations/home-office",
        )

    def _test_registered_interests(self, person: Person):
        self.assertQuerysetSize(person.registered_interests.all(), 36)
        interest = person.registered_interests.get(parliamentdotuk=10850)
        self.assertTrue("Payment: £205.86" in interest.description)
        self.assertEqual(interest.created, date(2024, 10, 2))
        self.assertTrue("4 Battle Bridge Lane" in interest.parent.description)

    def _test_subjects_of_interest(self, person: Person):
        self.assertQuerysetSize(person.subjects_of_interest.all(), 2)

    def _test_experiences(self, person: Person):
        self.assertQuerysetSize(person.experiences.all(), 4)
        exp = person.experiences.get(parliamentdotuk=2095)
        self.assertEqual(exp.title, "Trustee")
        self.assertEqual(exp.organisation.name, "National Library of Wales")
        self.assertEqual(exp.start, date(2012, 1, 1))
        self.assertEqual(exp.end, date(2021, 12, 1))

    def _test_contact(self, person: Person):
        self.assertEqual(
            person.web_addresses.get(type__name__contains="Twitter").url,
            "https://twitter.com/keir_starmer",
        )

        address = person.physical_addresses.get(type__name="Parliamentary office")
        self.assertEqual(address.address, "House of Commons, London")
        self.assertEqual(address.postcode, "SW1A 0AA")
        self.assertEqual(address.email, "keir.starmer.mp@parliament.uk")

    def _test_party_affiliations(self, person: Person):
        affiliation = person.party_affiliations.first()
        self.assertEqual(affiliation.party.name, "Labour")
        self.assertEqual(affiliation.start, date(2015, 5, 7))

    def _test_constituencies(self, person: Person):
        representation = person.constituencies.get(constituency__parliamentdotuk=3536)
        self.assertEqual(representation.start, date(2015, 5, 7))
        self.assertEqual(representation.end, date(2024, 5, 30))

        con = representation.constituency
        self.assertEqual(con.name, "Holborn and St Pancras")
        self.assertEqual(con.start, date(2010, 4, 13))
        self.assertEqual(con.end, date(2024, 5, 30))

    def _test_house_memberships(self, person: Person):
        house = person.house_memberships.first()

        self.assertEqual(house.house.name, "Commons")
        self.assertEqual(house.start, date(2015, 5, 7))

    def _test_elections_contested(self, person: Person):
        contested = person.contested_elections.first()

        self.assertEqual(contested.date, date(1997, 5, 1))
        self.assertEqual(contested.constituency.name, "Clwyd South")

    def _test_committees(self, person: Person):
        membership = person.committees.first()
        self.assertEqual(membership.start, date(2015, 7, 8))
        self.assertEqual(membership.end, date(2015, 10, 26))

        committee = membership.committee
        self.assertEqual(committee.name, "Home Affairs Committee")
