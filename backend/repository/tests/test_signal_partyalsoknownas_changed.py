from basetest.testcase import LocalTestCase
from repository.models import (
    Constituency,
    ConstituencyCandidate,
    ConstituencyResultDetail,
    Election,
    ElectionType,
    Party,
    PartyAlsoKnownAs,
    Person,
)
from repository.tests.data.create import (
    create_sample_constituency_candidate,
    create_sample_party,
)


class PartyAlsoKnownAsSignalTest(LocalTestCase):
    def setUp(self) -> None:
        self.party = create_sample_party("Liberal Democrats", 1)
        self.candidate = create_sample_constituency_candidate(
            party_name="LD",
            party=None,
        )

        self.other_candidate = create_sample_constituency_candidate(
            party_name="Lab",
            party=None,
        )

    def test_constituency_candidates_are_updated_when_partyalsoknownas_canonical_is_updated(
        self,
    ):
        self.assertIsNone(self.candidate.party)

        ld = PartyAlsoKnownAs.objects.create(alias="LD")
        ld.canonical = self.party
        ld.save()

        self.candidate.refresh_from_db()
        self.party.refresh_from_db()

        # Candidate party field should now be populated since PartyAlsoKnownAs.canonical was set.

        self.assertEqual(self.candidate.party.name, "Liberal Democrats")
        self.assertEqual(self.party.aliases.count(), 1)
        self.assertEqual(self.party.aliases.first().alias, "LD")

        # Make sure other candidates were not affected
        self.other_candidate.refresh_from_db()
        self.assertIsNone(self.other_candidate.party)
