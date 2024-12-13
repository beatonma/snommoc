from basetest.testcase import DatabaseTestCase
from repository.models.party import PartyTheme


class PartyThemeTests(DatabaseTestCase):
    def test_party_theme_rgb(self):
        theme = PartyTheme.objects.create(
            primary="#ff0000",
            on_primary="#00ff00",
            accent="#0000ff",
            on_accent="#f000f0",
        )

        self.assertEqual(theme.rgb_primary, "255 0 0")
        self.assertEqual(theme.rgb_on_primary, "0 255 0")
        self.assertEqual(theme.rgb_accent, "0 0 255")
        self.assertEqual(theme.rgb_on_accent, "240 0 240")
