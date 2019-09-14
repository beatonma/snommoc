import logging

from basetest.testcase import LocalTestCase
from repository.models.people import (
    GenericPersonOneToOneMixin,
    GenericPersonForeignKeyMixin,
)

log = logging.getLogger(__name__)


class BaseRepositoryLocalTestCase(LocalTestCase):
    """"""

    def tearDown(self) -> None:
        self.delete_instances_of(GenericPersonForeignKeyMixin, GenericPersonOneToOneMixin)
