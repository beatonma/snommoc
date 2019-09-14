import logging

from basetest.testcase import LocalTestCase

log = logging.getLogger(__name__)


class BaseRepositoryLocalTestCase(LocalTestCase):
    """"""

    def tearDown(self) -> None:
        pass
