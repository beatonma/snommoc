from unittest import (
    skipIf,
    skipUnless,
)

from django.test import TestCase

from basetest.args import RUNTESTS_CLARGS


class BaseTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None


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
