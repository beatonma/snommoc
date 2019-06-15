from unittest import skipIf

from django.test import TestCase

from basetest.args import RUNTESTS_CLARGS


class BaseTestCase(TestCase):
    def assert_nospace_equal(self, first, second, msg=''):
        """Assert that the two values are the same, ignoring spaces."""
        self.assertEqual(
            first.replace(r' ', ''),
            second.replace(r' ', ''),
            msg=msg)


class LocalTestCase(BaseTestCase):
    """Tests that use only local data - no external network calls!

    Always run when runtests.py is run.
    """
    pass


@skipIf(not RUNTESTS_CLARGS.network, reason='Network calls disabled by default')
class NetworkTestCase(BaseTestCase):
    """Tests that interact a remote server.

    Only run when specifically enabled via command line `-network` flag::
        runtests.py -network
    """
    pass
