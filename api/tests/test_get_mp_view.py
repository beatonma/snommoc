import json
import logging

from django.http import JsonResponse
from django.urls import reverse

from api import contract as api_contract
from api import endpoints as api_endpoints
from api.tests.views import with_api_key
# from api.views.people import (
#     VIEW_GET_ALL_MPS,
#     VIEW_GET_MP,
# )
from basetest.testcase import LocalTestCase
from repository.models import (
    Constituency,
    Mp,
    Party,
)
from repository.tests import values

log = logging.getLogger(__name__)


# TODO UPDATE VIEWS AND TESTS FOR DJANGO REST FRAMEWORK


class MpViewTest(LocalTestCase):
    @with_api_key
    def setUp(self, query):
        self.query = query
        Party.create(
            name=values.PARTY_NAME,
            short_name=values.PARTY_NAME_SHORT,
            long_name=values.PARTY_NAME_LONG)

        self.mp = Mp.create(
            name=values.EXAMPLE_NAME,
            # aliases=values.EXAMPLE_ALIASES,
            puk=values.EXAMPLE_PUK_ID,
            twfy=values.EXAMPLE_TWFY_ID,
            party=values.PARTY_NAME,
            constituency=values.CONSTITUENCY,
            phone_constituency=values.PHONE_CONSTITUENCY,
            phone_parliamentary=values.PHONE_PARLIAMENT,
            email=values.EMAIL,
            interests_countries=values.INTEREST_COUNTRY,
            interests_political=values.INTEREST_POLITICAL,
            weblinks=values.WEBLINKS,
            wikipedia_path=values.WIKIPEDIA
        )

        Constituency.objects.create(
            name=values.CONSTITUENCY,
            mp=self.mp,
        ).save()


class GetMpTest(MpViewTest):
    def test_get_mp_view_with_puk_id(self):
        response = self.client.get(
            reverse(api_endpoints.endpoint_list(api_endpoints.MP)),
            data={
                **self.query,
                api_contract.PARLIAMENTDOTUK_ID: values.EXAMPLE_PUK_ID
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        # self.assertIsInstance(response, JsonResponse)

        data = json.loads(response.content)
        self.assertEqual(data, values.MP_STRUCTURE)

    def test_get_mp_view_with_twfy_id(self):
        response = self.client.get(
            reverse(api_endpoints.endpoint_list(api_endpoints.MP)),
            data={
                **self.query,
                api_contract.THEYWORKFORYOU_ID: values.EXAMPLE_TWFY_ID
            })
        self.assertEqual(response.status_code, 200)
        # self.assertIsInstance(response, JsonResponse)

        data = json.loads(response.content)
        self.assertEqual(data, values.MP_STRUCTURE)

    def test_get_mp_view_with_puk_and_ids(self):
        response = self.client.get(
            reverse(api_endpoints.endpoint_list(api_endpoints.MP)),
            data={
                **self.query,
                api_contract.THEYWORKFORYOU_ID: values.EXAMPLE_TWFY_ID,
                api_contract.PARLIAMENTDOTUK_ID: values.EXAMPLE_PUK_ID
            })
        log.info(response.url)
        self.assertEqual(response.status_code, 200)
        # self.assertIsInstance(response, JsonResponse)

        data = json.loads(response.content)
        self.assertEqual(data, values.MP_STRUCTURE)

    def test_get_mp_view_with_no_id(self):
        """No id provided -> HttpResponseBadRequest"""
        response = self.client.get(
            reverse(api_endpoints.endpoint_list(api_endpoints.MP)),
            data=self.query
        )
        self.assertEqual(response.status_code, 400)

    def test_get_mp_view__without_api_key__should_return_http400(self):
        response = self.client.get(
            reverse(api_endpoints.endpoint_list(api_endpoints.MP))
        )
        self.assertEqual(response.status_code, 400)


class GetAllMPsTest(MpViewTest):
    def test_get_all_mps_view__is_correct(self):
        response = self.client.get(
            reverse(api_endpoints.endpoint_list(api_endpoints.MP)),
            data=self.query
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        mps = data.get(api_contract.MPS)
        self.assertEqual(len(mps), 1)
        self.assertEqual(mps[0].get(api_contract.NAME), values.EXAMPLE_NAME)

    def test_get_all_mps_view__without_api_key__should_return_http400(self):
        response = self.client.get(
            reverse(api_endpoints.endpoint_list(api_endpoints.MP))
        )
        self.assertEqual(response.status_code, 400)
