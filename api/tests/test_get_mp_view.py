import json

from django.http import JsonResponse

from api import contract as api_contract
from api.tests.views import with_api_key
from basetest.testcase import LocalTestCase
from repository.models import (
    Party,
    Constituency,
    Mp,
)
from repository.tests import values


class GetMpTest(LocalTestCase):
    @with_api_key
    def setUp(self, query):
        Party.objects.create(
            name=values.PARTY_NAME,
            short_name=values.PARTY_NAME_SHORT,
            long_name=values.PARTY_NAME_LONG).save()

        self.mp = Mp.create(
            name=values.EXAMPLE_NAME,
            aliases=values.EXAMPLE_ALIASES,
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

        self.query = query

    def test_get_mp_view_with_puk_id(self):
        response = self.client.get(
            '/get_mp',
            data={
                **self.query,
                api_contract.PARLIAMENTDOTUK_ID: values.EXAMPLE_PUK_ID
            })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        data = json.loads(response.content)
        self.assertEqual(data, values.MP_STRUCTURE)

    def test_get_mp_view_with_twfy_id(self):
        response = self.client.get(
            '/get_mp',
            data={
                **self.query,
                api_contract.THEYWORKFORYOU_ID: values.EXAMPLE_TWFY_ID
            })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        data = json.loads(response.content)
        self.assertEqual(data, values.MP_STRUCTURE)

    def test_get_mp_view_with_puk_and_ids(self):
        response = self.client.get(
            '/get_mp',
            data={
                **self.query,
                api_contract.THEYWORKFORYOU_ID: values.EXAMPLE_TWFY_ID,
                api_contract.PARLIAMENTDOTUK_ID: values.EXAMPLE_PUK_ID
            })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        data = json.loads(response.content)
        self.assertEqual(data, values.MP_STRUCTURE)

    def test_get_mp_view_with_no_id(self):
        """No id provided -> HttpResponseBadRequest"""
        response = self.client.get(
            '/get_mp',
            data={
                **self.query,
            })
        self.assertEqual(response.status_code, 400)
