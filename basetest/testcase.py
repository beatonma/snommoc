from unittest import skipIf

from django.test import TestCase

from basetest.args import RUNTESTS_CLARGS


class LocalTestCase(TestCase):
    """Tests that use only local data - no network calls!

    Always run when runtests.py is run.
    """
    pass


@skipIf(not RUNTESTS_CLARGS.network, reason='Network calls disabled by default')
class NetworkTestCase(TestCase):
    """Tests that interact a remote server.

    Only run when specifically enabled via command line `-network` flag::
        runtests.py -network
    """
    pass
