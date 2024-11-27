from django.test import TestCase


class BaseTestCase(TestCase):
    maxDiff = None

    def assertLengthEquals(self, collection, expected_length: int, msg=None):
        self.assertEqual(len(collection), expected_length, msg=msg)

    def assertNoneCreated(self, model_class, msg=None):
        self.assertEqual(model_class.objects.all().count(), 0, msg=msg)

    def assertQuerysetSize(self, queryset, expected_count: int, msg=None):
        self.assertEqual(queryset.all().count(), expected_count, msg=msg)


class LocalTestCase(BaseTestCase):
    """Tests that use only local data - no external network calls!"""

    pass
