import logging

from basetest.testcase import LocalTestCase
from repository.models import GenericPersonForeignKeyMixin

log = logging.getLogger(__name__)


class BaseRepositoryLocalTestCase(LocalTestCase):
    """"""

    def tearDown(self) -> None:
        GenericPersonForeignKeyMixin.objects.all().delete()
