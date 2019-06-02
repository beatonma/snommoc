from django.test import TestCase

from repository.models.people import NameAlias, PersonID, SuggestedAlias

EXAMPLE_NAME = 'John Bercow'
EXAMPLE_ALIAS = 'Jonny Bercow'
EXAMPLE_PUK_ID = 17
EXAMPLE_TWFY_ID = 10040


class PersonIdTest(TestCase):
    """"""
    def setUp(self) -> None:
        self.complete = PersonID.create(
            name=EXAMPLE_NAME,
            puk=EXAMPLE_PUK_ID,
            twfy=EXAMPLE_TWFY_ID)
        self.complete.save()

        self.puk_only = PersonID.create(
            name=EXAMPLE_NAME,
            puk=EXAMPLE_PUK_ID)

        self.twfy_only = PersonID.create(
            name=EXAMPLE_NAME,
            twfy=EXAMPLE_TWFY_ID)

        self.different_name = PersonID.create(
            name=EXAMPLE_ALIAS)
        self.different_name.save()

    def test_merge_puk_into_twfy(self):
        merged, _ = self.twfy_only.merge(self.puk_only)
        self.assertEqual(merged.theyworkforyou, EXAMPLE_TWFY_ID)
        self.assertEqual(merged.parliamentdotuk, EXAMPLE_PUK_ID)
        self.assertEqual(merged.name, EXAMPLE_NAME)

    def test_merge_twfy_into_puk(self):
        merged, _ = self.puk_only.merge(self.twfy_only)
        self.assertEqual(merged.theyworkforyou, EXAMPLE_TWFY_ID)
        self.assertEqual(merged.parliamentdotuk, EXAMPLE_PUK_ID)
        self.assertEqual(merged.name, EXAMPLE_NAME)

    def test_merge_different_name(self):
        """When merging PersonIDs with different names, suggest"""
        merged, suggested = self.complete.merge(self.different_name)
        self.assertEqual(merged.theyworkforyou, EXAMPLE_TWFY_ID)
        self.assertEqual(merged.parliamentdotuk, EXAMPLE_PUK_ID)
        self.assertEqual(merged.name, EXAMPLE_NAME)

        # suggested = SuggestedAlias.objects.get(personID=self.complete)
        self.assertEqual(suggested.alias.name, EXAMPLE_ALIAS)
        self.assertEqual(suggested.personID, self.complete)


class SuggestedAliasTest(TestCase):
    """"""
    def setUp(self) -> None:
        self.complete = PersonID.create(
            name=EXAMPLE_NAME,
            twfy=EXAMPLE_TWFY_ID)
        self.complete.save()

        self.different_name = PersonID.create(
            name=EXAMPLE_ALIAS,
            puk=EXAMPLE_PUK_ID)
        self.different_name.save()

        # Create SuggestedAlias by merging items with different names
        self.complete.merge(self.different_name)
        self.suggested = SuggestedAlias.objects.get(personID=self.complete)

    def test_setUp_is_correct(self):
        # Ensure suggestion exists in database
        self.assertEqual(len(SuggestedAlias.objects.all()), 1)

        # Ensure suggested alias does not have an associated PersonID
        self.assertIsNone(self.suggested.alias.personID)

    def test_namealias_approve_as_alias(self):
        self.suggested.approve_as_alias()

        updated_person_id = PersonID.objects.get(theyworkforyou=EXAMPLE_TWFY_ID)
        updated_alias = NameAlias.objects.get(personID=updated_person_id)

        # Confirm the association has been made
        self.assertEqual(updated_alias.personID, self.complete)

        # Ensure suggestion has been deleted from database
        self.assertEqual(len(SuggestedAlias.objects.all()), 0)

    def test_alias_approve_as_canonical(self):
        self.suggested.approve_as_canonical()

        updated_person_id = PersonID.objects.get(theyworkforyou=EXAMPLE_TWFY_ID)
        updated_alias = NameAlias.objects.get(personID=updated_person_id)

        # Ensure names have been swapped
        self.assertEqual(updated_person_id.name, EXAMPLE_ALIAS)
        self.assertEqual(updated_alias.name, EXAMPLE_NAME)

        # Confirm the association has been made
        self.assertEqual(self.suggested.alias.personID, self.complete)

        # Ensure suggestion has been deleted from database
        self.assertEqual(len(SuggestedAlias.objects.all()), 0)


class NameAliasTest(TestCase):
    """Tests for basic interactions of NameAlias and PersonID."""
    def setUp(self) -> None:
        self.canonical = PersonID.objects.create(
            name=EXAMPLE_NAME,
            theyworkforyou=EXAMPLE_TWFY_ID,
            parliamentdotuk=EXAMPLE_PUK_ID)
        self.canonical.save()

        NameAlias.objects.create(
            name=EXAMPLE_NAME,
            personID=self.canonical).save()

        NameAlias.objects.create(
            name=EXAMPLE_ALIAS,
            personID=self.canonical).save()

        # Alias with no association to a canonical PersonID
        NameAlias.objects.create(
            name='Jonas Barcow').save()

    def test_get_canonical_from_alias(self):
        self.assertEquals(
            NameAlias.objects.get(name=EXAMPLE_NAME).canonical,
            EXAMPLE_NAME)
        self.assertEquals(
            NameAlias.objects.get(name=EXAMPLE_ALIAS).canonical,
            EXAMPLE_NAME)

        self.assertNotEqual(
            NameAlias.objects.get(name='Jonas Barcow').canonical,
            EXAMPLE_NAME)

    def test_get_aliases_from_canonical(self):
        self.assertListEqual(
            self.canonical.aliases,
            [EXAMPLE_NAME, EXAMPLE_ALIAS])
