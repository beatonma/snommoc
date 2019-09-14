import json

from django.http import JsonResponse
from django.urls import reverse

from api import contract
from api import endpoints as api_endpoints
from api.tests.views import with_api_key
from basetest.testcase import LocalTestCase
from repository.models import Party
from repository.tests import values


# TODO UPDATE TESTS FOR DJANGO REST FRAMEWORK


class GetPartiesTest(LocalTestCase):
    @with_api_key
    def setUp(self, query):
        self.query = query
        Party.create(
            name=values.PARTY_NAME,
            short_name=values.PARTY_NAME_SHORT,
            long_name=values.PARTY_NAME_LONG)

    def test_get_parties_view(self):
        response = self.client.get(
            reverse(api_endpoints.endpoint_list(api_endpoints.PARTY)),
            data={**self.query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        data = json.loads(response.content)
        parties = data.get(contract.PARTIES)
        self.assertIsInstance(parties, list)
        self.assertEqual(len(parties), 1)
        self.assertEqual(parties[0].get(contract.PARTY), values.PARTY_NAME)
