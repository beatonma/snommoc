from basetest.args import RUNTESTS_CLARGS
from basetest.testcase import NetworkTestCase


class NetworkExampleTestCase(NetworkTestCase):
    """Ensure that network test only runs when network arg is set"""
    def test_this_should_not_run_if_network_arg_not_set(self):
        self.assertTrue(RUNTESTS_CLARGS.network)
