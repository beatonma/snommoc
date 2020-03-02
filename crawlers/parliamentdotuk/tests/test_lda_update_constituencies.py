import datetime
import logging
from unittest import mock

import requests

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda import lda_client
from crawlers.parliamentdotuk.tasks.lda.update_constituencies import (
    update_constituencies,
)
from repository.models import Constituency

from .data_lda_update_constituencies import EXAMPLE_RESPONSE
from .mock import MockJsonResponse

log = logging.getLogger(__name__)


def get_mock_json_response(*args, **kwargs):
    return MockJsonResponse(args[0], EXAMPLE_RESPONSE, 200)


class UpdateConstituenciesTest(LocalTestCase):
    """"""

    @mock.patch.object(
        requests, 'get',
        mock.Mock(side_effect=get_mock_json_response),
    )
    @mock.patch.object(
        lda_client, 'get_next_page_url',
        mock.Mock(side_effect=lambda x: None)
    )
    def test_update_constituencies(self):
        self.assertEqual(len(Constituency.objects.all()), 0)
        update_constituencies()
        new_constituencies = Constituency.objects.all()
        self.assertEqual(len(new_constituencies), 10)

        aberavon: Constituency = new_constituencies.get(parliamentdotuk=146747)
        self.assertEqual(aberavon.name, 'Aberavon')
        self.assertEqual(aberavon.constituency_type, 'County')
        self.assertEqual(aberavon.gss_code, 'W07000049')
        self.assertEqual(aberavon.ordinance_survey_name, '')
        self.assertEqual(aberavon.start, datetime.date(year=2010, month=5, day=6))
        self.assertEqual(aberavon.end, None)
        self.assertEqual(aberavon.parliamentdotuk, 146747)

        aberconwy: Constituency = new_constituencies.get(parliamentdotuk=146748)
        self.assertEqual(aberconwy.name, 'Aberconwy')
        self.assertEqual(aberconwy.constituency_type, 'County')
        self.assertEqual(aberconwy.gss_code, 'W07000058')
        self.assertEqual(aberconwy.ordinance_survey_name, 'Aberconwy Co Const')
        self.assertEqual(aberconwy.start, datetime.date(year=2010, month=5, day=6))
        self.assertEqual(aberconwy.end, None)
        self.assertEqual(aberconwy.parliamentdotuk, 146748)

        aberdare: Constituency = new_constituencies.get(parliamentdotuk=143467)
        self.assertEqual(aberdare.name, 'Aberdare')
        self.assertEqual(aberdare.constituency_type, 'Borough')
        self.assertEqual(aberdare.gss_code, '')
        self.assertEqual(aberdare.ordinance_survey_name, '')
        self.assertEqual(aberdare.start, datetime.date(year=1974, month=2, day=28))
        self.assertEqual(aberdare.end, datetime.date(year=1983, month=6, day=9))
        self.assertEqual(aberdare.parliamentdotuk, 143467)

    def tearDown(self) -> None:
        Constituency.objects.all().delete()
