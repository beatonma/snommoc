import logging
from unittest import (
    skipUnless,
)

from django.test import TestCase

from basetest.args import RUNTESTS_CLARGS


log = logging.getLogger(__name__)


class BaseTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def delete_instances_of(self, *classList):
        for cls in classList:
            try:
                cls.objects.all().delete()
            except Exception as e:
                log.warning(e)

    def assertEqualIgnoreCase(self, first: str, second: str, msg=None):
        self.assertEqual(first.lower(), second.lower(), msg=msg)

    def assertLengthEquals(self, collection, expected_length: int, msg=None):
        self.assertEqual(len(collection), expected_length, msg=msg)

    def assertEmpty(self, collection, msg=None):
        self.assertLengthEquals(collection, 0, msg=msg)

    def assertNoneCreated(self, model_class, msg=None):
        self.assertEqual(model_class.objects.all().count(), 0, msg=msg)

    def assertQuerysetSize(self, queryset, expected_length: int, msg=None):
        self.assertLengthEquals(queryset.all(), expected_length, msg=msg)


class LocalTestCase(BaseTestCase):
    """Tests that use only local data - no external network calls!

    Always run when runtests.py is run.
    """
    pass


@skipUnless(RUNTESTS_CLARGS.network, reason='Network calls disabled by default')
class NetworkTestCase(BaseTestCase):
    """Tests that interact a remote server.

    Only run when specifically enabled via command line `-network` flag::
        runtests.py -network
    """
    pass
