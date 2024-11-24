from basetest.testcase import LocalTestCase
from repository.models import (
    Constituency,
    Election,
    ElectionType,
    Person,
    PersonAlsoKnownAs,
)
from repository.resolution.members import normalize_name
from repository.tests.data.create import (
    create_constituency_result,
    create_sample_constituencies,
    create_sample_elections,
    create_sample_person,
)


class MemberResolutionTest(LocalTestCase):
    mp = None
    constituency = None
    election = None

    def setUp(self) -> None:
        create_sample_constituencies()
        create_sample_elections()

        self.election = Election.objects.get(pk=397, name="2019 General Election")

        self.mp = create_sample_person(4467, "Drew Hendry")
        self.constituency = Constituency.objects.get(
            pk=145021,
            name="Inverness, Nairn, Badenoch and Strathspey",
        )
        self.constituency.mp = self.mp
        self.constituency.save()

        create_constituency_result(self.constituency, self.election, self.mp)

    def test_get_normalized_name__removes_honorifics(self):
        self.assertEqual(normalize_name("Rt Hon Alistair Darling"), "Alistair Darling")
        self.assertEqual(normalize_name("Sir Christopher Chope"), "Christopher Chope")

        # Check that name beginning with an honorific ("Sir") are unaffected.
        self.assertEqual(normalize_name("Sirius Snape"), "Sirius Snape")

    def test_get_normalized_name__normalises_whitespace(self):
        self.assertEqual(normalize_name("Caroline   Lucas"), "Caroline Lucas")
        self.assertEqual(normalize_name("Lucas,   Caroline"), "Caroline Lucas")

        self.assertEqual(normalize_name(" Caroline Lucas "), "Caroline Lucas")
        self.assertEqual(normalize_name(" Lucas, Caroline "), "Caroline Lucas")

    def test_get_normalized_name__normalizes_name_ordering(self):
        """Names in the format `Surname, Forename` should be rearranged to `Forename Surname`"""
        self.assertEqual(normalize_name("Caroline Lucas"), "Caroline Lucas")
        self.assertEqual(normalize_name("Lucas, Caroline"), "Caroline Lucas")

    def tearDown(self) -> None:
        self.mp = None
        self.constituency = None
        self.election = None

        self.delete_instances_of(
            Constituency,
            Election,
            ElectionType,
            Person,
            PersonAlsoKnownAs,
        )
