from unittest import TestCase

import pytest
from django.test import TestCase as DjangoTestCase


class SimpleTestCase(TestCase):
    """Base class for tests that don't need database access."""

    maxDiff = None

    def assertLengthEquals(self, collection, expected_length: int, msg=None):
        self.assertEqual(len(collection), expected_length, msg=msg)


@pytest.mark.skipif("config.getoption('skip_database')")
class DatabaseTestCase(SimpleTestCase, DjangoTestCase):
    """Base class for tests that need database access."""

    def assertNoneCreated(self, model_class, msg=None):
        self.assertEqual(model_class.objects.all().count(), 0, msg=msg)

    def assertQuerysetSize(self, queryset, expected_count: int, msg=None):
        self.assertEqual(queryset.all().count(), expected_count, msg=msg)
