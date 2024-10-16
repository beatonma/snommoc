import datetime
from unittest.mock import patch

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.membersdataplatform import active_members
from crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client import (
    AddressResponseData,
    BasicInfoResponseData,
    CommitteeResponseData,
    ConstituencyResponseData,
    ContestedElectionResponseData,
    DeclaredInterestCategoryResponseData,
    ExperiencesResponseData,
    HouseMembershipResponseData,
    PartyResponseData,
    PostResponseData,
    SpeechResponseData,
    SubjectsOfInterestResponseData,
)
from repository.models import (
    Committee,
    Constituency,
    ConstituencyResult,
    Country,
    DeclaredInterest,
    DeclaredInterestCategory,
    Election,
    Experience,
    ExperienceCategory,
    GovernmentPost,
    GovernmentPostMember,
    House,
    HouseMembership,
    MaidenSpeech,
    OppositionPost,
    OppositionPostMember,
    ParliamentaryPost,
    ParliamentaryPostMember,
    ParliamentarySession,
    Party,
    PartyAssociation,
    Person,
    PhysicalAddress,
    SubjectOfInterest,
    SubjectOfInterestCategory,
    WebAddress,
)
from repository.models.committees import (
    CommitteeChair,
    CommitteeMember,
)
from repository.models.constituency import UnlinkedConstituency
from repository.models.election import ContestedElection, ElectionType
from repository.models.geography import Town
from repository.models.houses import (
    HOUSE_OF_COMMONS,
    HOUSE_OF_LORDS,
)
from repository.tests import values
from .data_mdp_update_active_mps import *


class MdpUpdateActiveMpsTest(LocalTestCase):
    def setUp(self) -> None:
        commons, _ = House.objects.update_or_create(name=HOUSE_OF_COMMONS)
        House.objects.update_or_create(name=HOUSE_OF_LORDS)

        Constituency.objects.create(
            parliamentdotuk=146260,
            name="Stockton South",
            start=datetime.date(1983, 6, 9),
            end=datetime.date(1997, 5, 1),
        )

        Constituency.objects.create(
            parliamentdotuk=13124,
            name="Thornaby",
        )

        self.person = Person.objects.create(
            parliamentdotuk=965,  # ID for Lord Wrigglesworth, used in SAMPLE_BIOGRAPHY_RESPONSE
            name=values.EXAMPLE_NAME,
            active=True,
            house=commons,
        )

    def test__update_house_membership(self):
        house_memberships = [
            HouseMembershipResponseData(hm) for hm in SAMPLE_HOUSE_MEMBERSHIP
        ]

        active_members._update_house_membership(self.person, house_memberships)

        lords_membership = HouseMembership.objects.get(
            person=self.person, house=House.objects.get(name=HOUSE_OF_LORDS)
        )
        self.assertEqual(
            lords_membership.start, datetime.date(year=2013, month=9, day=5)
        )
        self.assertIsNone(lords_membership.end)

        commons_membership = HouseMembership.objects.get(
            person=self.person, house=House.objects.get(name=HOUSE_OF_COMMONS)
        )
        self.assertEqual(
            commons_membership.start, datetime.date(year=1974, month=2, day=28)
        )
        self.assertEqual(
            commons_membership.end, datetime.date(year=1987, month=6, day=11)
        )

    def test__update_historical_constituencies(self):
        historical_constituencies = [
            ConstituencyResponseData(c) for c in SAMPLE_HISTORICAL_CONSTITUENCIES
        ]

        active_members._update_historical_constituencies(
            self.person, historical_constituencies
        )

        stockton_south = Constituency.objects.get(parliamentdotuk=146260)
        result = ConstituencyResult.objects.get(
            constituency=stockton_south, start=datetime.date(year=1983, month=6, day=9)
        )
        self.assertEqual(result.election.name, "1983 General Election")
        self.assertEqual(result.election.date, datetime.date(year=1983, month=6, day=9))
        self.assertEqual(result.election.election_type.name, "General Election")
        self.assertEqual(result.end, datetime.date(year=1987, month=6, day=11))

        self.assertEqual(
            len(ConstituencyResult.objects.filter(constituency__name="Thornaby")), 3
        )

    def test__update_basic_details(self):
        basic_info = BasicInfoResponseData(SAMPLE_BASIC_INFO)
        active_members._update_basic_details(self.person, basic_info)

        self.assertEqualIgnoreCase(self.person.additional_name, "Julie")
        self.assertEqualIgnoreCase(self.person.given_name, "Diane")
        self.assertEqualIgnoreCase(self.person.family_name, "Abbott")
        self.assertEqualIgnoreCase(self.person.town_of_birth.name, "London")
        self.assertEqualIgnoreCase(self.person.country_of_birth.name, "England")

    def test__update_committees(self):
        committees = [CommitteeResponseData(c) for c in SAMPLE_COMMITTEES]
        active_members._update_committees(self.person, committees)

        self.assertEqual(len(Committee.objects.all()), 18)
        self.assertEqual(len(CommitteeMember.objects.filter(person=self.person)), 23)
        self.assertEqual(
            len(CommitteeChair.objects.filter(member__person=self.person)), 2
        )

        admin_committee = Committee.objects.get(parliamentdotuk=2)
        admin_committee_chair = CommitteeChair.objects.get(
            member__committee=admin_committee,
            start=datetime.date(year=2017, month=11, day=6),
        )
        self.assertEqual(
            admin_committee_chair.end, datetime.date(year=2019, month=11, day=6)
        )

    def test__update_declared_interests(self):
        interest_categories = [
            DeclaredInterestCategoryResponseData(c) for c in SAMPLE_INTERESTS
        ]
        active_members._update_declared_interests(self.person, interest_categories)

        self.assertLengthEquals(DeclaredInterestCategory.objects.all(), 3)

        directorships = DeclaredInterestCategory.objects.get(parliamentdotuk=1)
        self.assertLengthEquals(
            DeclaredInterest.objects.filter(category=directorships), 4
        )

        durham_group_estates = DeclaredInterest.objects.get(parliamentdotuk=12485)
        self.assertEqual(durham_group_estates.person, self.person)
        self.assertEqual(
            durham_group_estates.description, "Director, Durham Group Estates Ltd"
        )
        self.assertEqual(
            durham_group_estates.created, datetime.date(year=2013, month=12, day=2)
        )
        self.assertFalse(durham_group_estates.registered_late)
        self.assertIsNone(durham_group_estates.amended)
        self.assertIsNone(durham_group_estates.deleted)

        machine_delta = DeclaredInterest.objects.get(parliamentdotuk=24419)
        self.assertEqual(
            machine_delta.description,
            "Machine Delta (a division of Caspian Learning Ltd providing intelligent"
            " quality assurance using artificial intelligence)",
        )
        self.assertEqual(
            machine_delta.created, datetime.date(year=2015, month=12, day=31)
        )
        self.assertEqual(
            machine_delta.amended, datetime.date(year=2018, month=6, day=21)
        )

    def test__update_opposition_posts(self):
        opposition_posts = [PostResponseData(p) for p in SAMPLE_OPPOSITION_POSTS]
        active_members._update_opposition_posts(self.person, opposition_posts)

        self.assertLengthEquals(OppositionPost.objects.all(), 4)
        self.assertLengthEquals(
            OppositionPostMember.objects.filter(person=self.person), 4
        )

        shadow_home_secretary = OppositionPost.objects.get(parliamentdotuk=1171)
        self.assertEqual(shadow_home_secretary.name, "Shadow Home Secretary")
        self.assertEqual(shadow_home_secretary.hansard_name, "Shadow Home Secretary")

        membership = OppositionPostMember.objects.get(post=shadow_home_secretary)
        self.assertEqual(membership.person, self.person)
        self.assertEqual(membership.start, datetime.date(year=2016, month=10, day=6))
        self.assertIsNone(membership.end)

    def test__update_parliamentary_posts(self):
        parliamentary_posts = [PostResponseData(p) for p in SAMPLE_PARLIAMENTARY_POSTS]
        active_members._update_parliamentary_posts(self.person, parliamentary_posts)

        self.assertLengthEquals(ParliamentaryPost.objects.all(), 1)
        self.assertLengthEquals(
            ParliamentaryPostMember.objects.filter(person=self.person), 1
        )

        labour_nec = ParliamentaryPost.objects.get(parliamentdotuk=803)
        self.assertEqual(
            labour_nec.name, "Member, Labour Party National Executive Committee"
        )
        self.assertIsNone(labour_nec.hansard_name)

        member = ParliamentaryPostMember.objects.get(post=labour_nec)
        self.assertEqual(member.person, self.person)
        self.assertEqual(member.start, datetime.date(year=1994, month=1, day=1))
        self.assertEqual(member.end, datetime.date(year=1997, month=1, day=1))

        self.assertEqual(member.person, self.person)

    def test__update_addresses(self):
        addresses = [AddressResponseData(a) for a in SAMPLE_ADDRESSES]
        active_members._update_addresses(self.person, addresses)

        self.assertLengthEquals(PhysicalAddress.objects.all(), 2)
        self.assertLengthEquals(WebAddress.objects.all(), 1)

        parliamentary_address = PhysicalAddress.objects.get(postcode="SW1A 0AA")
        self.assertEqual(parliamentary_address.address, "House of Commons, London")
        self.assertEqual(parliamentary_address.description, "Parliamentary")
        self.assertEqual(parliamentary_address.phone.as_national, "020 7219 5018")
        self.assertIsNone(parliamentary_address.fax)
        self.assertEqual(parliamentary_address.email, "annie.winsbury@parliament.uk")

        constituency_address = PhysicalAddress.objects.get(postcode="KT21 2DB")
        self.assertEqual(constituency_address.description, "Constituency")
        self.assertEqual(
            constituency_address.address,
            "Mole Valley Conservative Association, 212 Barnett Wood Lane, Ashtead",
        )
        self.assertEqual(
            constituency_address.email, "office@molevalleyconservatives.org.uk"
        )
        self.assertEqual(constituency_address.phone.as_national, "01306 883312")

        website = WebAddress.objects.get(description="Website")
        self.assertEqual(website.url, "http://www.molevalleyconservatives.org.uk/")

    def test__update_maiden_speeches(self):
        speeches = [SpeechResponseData(s) for s in SAMPLE_MAIDEN_SPEECHES]
        active_members._update_maiden_speeches(self.person, speeches)

        lords = MaidenSpeech.objects.get(house__name="Lords")
        self.assertEqual(lords.date, datetime.date(year=2013, month=10, day=24))
        self.assertIsNone(lords.hansard)
        self.assertIsNone(lords.subject)

        commons = MaidenSpeech.objects.get(house__name="Commons")
        self.assertEqual(commons.date, datetime.date(year=1974, month=3, day=25))
        self.assertEqual(commons.hansard, "871 c77-9")
        self.assertEqual(commons.subject, "Some subject")

    def test__update_party_associations(self):
        parties = [PartyResponseData(p) for p in SAMPLE_PARTY_ASSOCIATIONS]
        active_members._update_party_associations(self.person, parties)

        self.assertLengthEquals(PartyAssociation.objects.filter(person=self.person), 3)

        labour = PartyAssociation.objects.get(party__name="Labour")
        self.assertEqual(labour.person, self.person)
        self.assertEqual(labour.start, datetime.date(year=1974, month=2, day=28))
        self.assertEqual(labour.end, datetime.date(year=1981, month=3, day=2))
        self.assertEqual(labour.party.parliamentdotuk, 15)

        libdem = PartyAssociation.objects.get(party__name="Liberal Democrat")
        self.assertEqual(libdem.person, self.person)
        self.assertEqual(libdem.start, datetime.date(year=1988, month=3, day=3))
        self.assertIsNone(libdem.end)
        self.assertEqual(libdem.party.parliamentdotuk, 17)

    def test__update_government_posts(self):
        government_posts = [PostResponseData(p) for p in SAMPLE_GOVERNMENT_POSTS]
        active_members._update_government_posts(self.person, government_posts)

        pm = GovernmentPost.objects.get(parliamentdotuk=661)
        self.assertEqual(
            pm.name,
            "Prime Minister, First Lord of the Treasury and Minister for the Civil"
            " Service",
        )
        self.assertEqual(pm.hansard_name, "The Prime Minister")

        pm_member = GovernmentPostMember.objects.get(post=pm)
        self.assertEqual(pm_member.start, datetime.date(year=2019, month=7, day=24))
        self.assertIsNone(pm_member.end)

        sec_of_state = GovernmentPost.objects.get(parliamentdotuk=1128)
        self.assertEqual(
            sec_of_state.name, "Secretary of State for Foreign and Commonwealth Affairs"
        )
        self.assertEqual(
            sec_of_state.hansard_name,
            "Secretary of State for Foreign and Commonwealth Affairs",
        )

        sec_of_state_member = GovernmentPostMember.objects.get(post=sec_of_state)
        self.assertEqual(
            sec_of_state_member.start, datetime.date(year=2016, month=7, day=13)
        )
        self.assertEqual(
            sec_of_state_member.end, datetime.date(year=2018, month=7, day=9)
        )
        self.assertEqual(sec_of_state_member.person, self.person)

    def test__update_experiences(self):
        experiences = [ExperiencesResponseData(e) for e in SAMPLE_EXPERIENCES]
        active_members._update_experiences(self.person, experiences)

        self.assertLengthEquals(Experience.objects.all(), 12)
        uk_land_estates = Experience.objects.get(organisation="UK Land Estates")
        self.assertEqual(uk_land_estates.person, self.person)
        self.assertEqual(uk_land_estates.category.name, "Non political")
        self.assertEqual(uk_land_estates.title, "Founding Chairman")
        self.assertEqual(
            uk_land_estates.start, datetime.date(year=1995, month=12, day=25)
        )
        self.assertEqual(
            uk_land_estates.end, datetime.date(year=2009, month=12, day=25)
        )

    def test__update_elections_contested(self):
        Constituency.objects.create(
            parliamentdotuk=1,
            name="Clwyd South",
        )

        contested = [
            ContestedElectionResponseData(e) for e in SAMPLE_ELECTIONS_CONTESTED
        ]
        active_members._update_elections_contested(self.person, contested)

        election = Election.objects.get(parliamentdotuk=15)
        constituency = Constituency.objects.get(name="Clwyd South")

        ge = ContestedElection.objects.get(election__name="1997 General Election")
        self.assertEqual(ge.election, election)
        self.assertEqual(ge.election.date, datetime.date(year=1997, month=5, day=1))
        self.assertEqual(ge.constituency, constituency)

        self.assertEqual(ge.election.election_type.name, "General Election")

        self.assertEqual(self.person.contestedelection_set.first(), ge)

        unlinked_constituency = UnlinkedConstituency.objects.first()
        self.assertEqual(unlinked_constituency.name, "Some Unknown Constituency")
        self.assertEqual(unlinked_constituency.person, self.person)
        self.assertEqual(unlinked_constituency.election.name, "1998 General Election")

    def test__update_subjects_of_interest(self):
        experiences = [
            SubjectsOfInterestResponseData(e) for e in SAMPLE_BIOGRAPHY_ENTRIES
        ]
        active_members._update_subjects_of_interest(self.person, experiences)

        self.assertLengthEquals(SubjectOfInterestCategory.objects.all(), 3)
        self.assertLengthEquals(SubjectOfInterest.objects.all(), 3)

        world_areas_category = SubjectOfInterestCategory.objects.get(
            title="Concerns: World Areas"
        )
        world_areas_subject = SubjectOfInterest.objects.get(
            category=world_areas_category
        )

        self.assertEqual(world_areas_subject.person, self.person)
        self.assertEqual(
            world_areas_subject.subject, "India; Poland; South East Asia; Turkey; USA"
        )

    @patch(
        "crawlers.parliamentdotuk.tasks.membersdataplatform.mdp_client.get_json",
        side_effect=lambda *args, **kwargs: SAMPLE_BIOGRAPHY_RESPONSE,
    )
    def test_update_active_member_details(self, *args, **kwargs):
        """Check that all of the update methods have been called.

        The other tests here ensure the methods work correctly so we just need to
        check that the expected models were created to verify that the methods
        were actually called."""

        puk = 965

        active_members.update_active_member_details(cache=None)

        person = Person.objects.get(parliamentdotuk=puk)

        # Basic details
        self.assertEqualIgnoreCase(person.given_name, "Ian")
        self.assertEqualIgnoreCase(person.family_name, "Wrigglesworth")
        self.assertIsNone(person.town_of_birth)
        self.assertIsNone(person.country_of_birth)

        # House memberships
        self.assertQuerysetSize(person.housemembership_set, 2)

        # Historical constituencies
        self.assertQuerysetSize(person.constituencyresult_set, 4)

        # Historical party memberships
        self.assertQuerysetSize(person.parties, 3)

        # Maiden speeches
        self.assertQuerysetSize(person.maidenspeech_set, 2)

        # Committees
        self.assertQuerysetSize(person.committeemember_set, 5)

        # Addresses
        self.assertQuerysetSize(person.physicaladdress_set, 1)
        self.assertQuerysetSize(person.webaddress_set, 1)

        # Declared interests
        self.assertQuerysetSize(person.declaredinterest_set, 9)

        # Experiences
        self.assertQuerysetSize(person.experience_set, 12)

        # Subjects of interest
        self.assertQuerysetSize(person.subjectofinterest_set, 3)

        # Government posts
        self.assertQuerysetSize(person.governmentpostmember_set, 2)

        # Parliamentary posts
        self.assertQuerysetSize(person.parliamentarypostmember_set, 1)

        # Opposition posts
        self.assertQuerysetSize(person.oppositionpostmember_set, 4)

        # Elections contested
        self.assertQuerysetSize(person.contestedelection_set, 1)

    def tearDown(self) -> None:
        self.delete_instances_of(
            Committee,
            CommitteeChair,
            CommitteeMember,
            Constituency,
            ConstituencyResult,
            ContestedElection,
            Country,
            DeclaredInterestCategory,
            Election,
            ElectionType,
            ExperienceCategory,
            GovernmentPost,
            House,
            HouseMembership,
            MaidenSpeech,
            OppositionPost,
            ParliamentaryPost,
            ParliamentarySession,
            Party,
            Person,
            SubjectOfInterestCategory,
            Town,
        )
