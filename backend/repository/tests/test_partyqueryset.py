from basetest.testcase import DatabaseTestCase
from repository.models import Party
from repository.tests.data.create import create_sample_party


class PartyQuerySetTests(DatabaseTestCase):
    def test_resolve(self):
        resolve = Party.objects.resolve
        party = create_sample_party("Conservative")

        # Resolve existing party by ID
        self.assertEqual((party, False), resolve(parliamentdotuk=party.parliamentdotuk))
        # Resolve existing party by name
        self.assertEqual((party, False), resolve(name=party.name))

        lib_dem = Party(parliamentdotuk=17, name="Liberal Democrat")
        # Returns None when party does not exist and not enough info to create it
        self.assertEqual(
            (None, False),
            resolve(parliamentdotuk=lib_dem.parliamentdotuk),
        )
        self.assertEqual((None, False), resolve(name=lib_dem.name))

        # Creates party when enough info to do so
        self.assertEqual(
            (lib_dem, True),
            resolve(
                parliamentdotuk=lib_dem.parliamentdotuk,
                name=lib_dem.name,
            ),
        )

        # Previous queries now return the created party
        self.assertEqual(
            (lib_dem, False),
            resolve(parliamentdotuk=lib_dem.parliamentdotuk),
        )
        self.assertEqual((lib_dem, False), resolve(name=lib_dem.name))

    def test_resolve__labour(self):
        """Special cases because Labour and Labour (Co-op) use the same parliamentdotuk ID."""
        resolve = Party.objects.resolve

        labour, _ = resolve(parliamentdotuk=15, name="Labour")
        labour_coop, _ = resolve(parliamentdotuk=15, name="Labour Co-op")

        self.assertNotEqual(labour.parliamentdotuk, labour_coop.parliamentdotuk)

        self.assertEqual((labour, False), resolve(name="Labour"))
        self.assertEqual((labour_coop, False), resolve(name="Labour coop"))
        self.assertEqual((labour_coop, False), resolve(name="Labour co-op"))
        self.assertEqual((labour_coop, False), resolve(name="Labour (coop)"))
        self.assertEqual((labour_coop, False), resolve(name="Labour (co-op)"))

    def test_search(self):
        sf = create_sample_party("Sinn Féin")
        snp = create_sample_party("Scottish National Party", short_name="SNP")

        self.assertEqual(Party.objects.search("fein").first(), sf)
        self.assertEqual(Party.objects.search("scottish").first(), snp)
        self.assertEqual(Party.objects.search("snp").first(), snp)
