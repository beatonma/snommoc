from basetest.testcase import DatabaseTestCase, SimpleTestCase
from repository.models import Organisation


class OrganisationTests(DatabaseTestCase):
    @staticmethod
    def _get_or_create(name: str, url: str = None):
        return Organisation.objects.get_or_create(
            name=name,
            defaults={"url": url} if url else None,
        )

    @staticmethod
    def _update_or_create(name: str, url: str = None):
        return Organisation.objects.update_or_create(
            name=name,
            defaults={"url": url} if url else None,
        )

    def test_organisation_resolves_name_via_slug(self):
        self._get_or_create("NO to A.V.")
        self._get_or_create("No to AV")

        self.assertQuerysetSize(Organisation.objects.all(), 1)
        self.assertEqual(Organisation.objects.first().name, "NO to AV")

        ofcom, _ = self._get_or_create("Ofcom")
        ofcom2, _ = self._get_or_create("OFCOM")
        self.assertEqual(ofcom.pk, ofcom2.pk)
        self.assertQuerysetSize(Organisation.objects.all(), 2)

        self.assertEqual(Organisation.objects.get(name="ofcom").pk, ofcom.pk)
        self.assertEqual(Organisation.objects.get(name="oFCOm").pk, ofcom.pk)

        # update_or_create also resolves correctly
        updated, _created = self._update_or_create(
            "ofcom", url="https://ofcom.whatever"
        )
        self.assertEqual(updated.pk, ofcom.pk)
        self.assertEqual(
            Organisation.objects.get(name="OFCOM").url,
            "https://ofcom.whatever",
        )


class OrganisationNormaliseNameTests(SimpleTestCase):
    @staticmethod
    def normalise(name: str):
        return Organisation.normalise_name(name)

    def test_name_normalisation(self):
        data: list[tuple[str, str]] = [
            (
                "Directors Cut Productions LTD.",
                "Directors Cut Productions Ltd",
            ),
            (
                "Equality and Human Rights commission",
                "Equality & Human Rights Commission",
            ),
            ("F.C.O.", "FCO"),
            ("Abbey National Plc", "Abbey National PLC"),
            ("10, Downing Street", "10 Downing Street"),
            (
                "Dept of Business, Energy and Industrial Strategy (BEIS)",
                "Department of Business, Energy & Industrial Strategy (BEIS)",
            ),
            ("Conservative Research Dept", "Conservative Research Department"),
            ("Conservative Research Dept.", "Conservative Research Department"),
            ("Labour Party N.E.C.", "Labour Party NEC"),
        ]

        for name, expected in data:
            self.assertEqual(self.normalise(name), expected)
