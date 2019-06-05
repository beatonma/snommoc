from django.test import TestCase


class LocalTestCase(TestCase):
    """Tests that use only local data - no network calls."""
    pass


class NetworkTestCase(TestCase):
    """Tests that contact a remote server."""
    pass
