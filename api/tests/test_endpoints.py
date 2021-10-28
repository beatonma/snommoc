from django.contrib.auth.models import User
from django.urls import reverse

from api import endpoints
from api.models import ApiKey, grant_read_snommoc_api
from basetest.test_util import create_sample_user
from basetest.testcase import LocalApiTestCase
from repository.models import (
    Bill,
    BillType,
    CommonsDivision,
    Constituency,
    Election,
    ElectionType,
    LordsDivision,
    ParliamentarySession,
    Party,
    Person,
)
from repository.tests.data.create import (
    create_constituency_result_detail,
    create_sample_bill,
    create_sample_commons_division,
    create_sample_constituency,
    create_sample_election,
    create_sample_lords_division,
    create_sample_party,
    create_sample_person,
)
from social.models.token import SignInServiceProvider, UserToken


class EndpointTests(LocalApiTestCase):
    """Ensure endpoints return expected status and content type."""

    def setUp(self) -> None:
        user_with_permission = create_sample_user(username="endpoints")
        grant_read_snommoc_api(user_with_permission)
        self.client.force_login(user_with_permission)

    def test_ping(self):
        response = self.client.get(reverse(endpoints.PING))
        self.assertResponseOK(response)

    def test_endpoint_zeitgeist(self):
        response = self.client.get(reverse(endpoints.ZEITGEIST))

        self.assertResponseOK(response)
        self.assertIsJsonResponse(response)

    def tearDown(self) -> None:
        self.delete_instances_of(
            ApiKey,
            User,
            SignInServiceProvider,
            UserToken,
        )


class QueryEndpointTests(LocalApiTestCase):
    """Query endpoints should return JSON content with status=200 when the requested object exists, otherwise 404."""

    def setUp(self) -> None:
        user_with_permission = create_sample_user(username="endpoints")
        grant_read_snommoc_api(user_with_permission)
        self.client.force_login(user_with_permission)

    def _assert_response_json_ok(self, url):
        """Assert that the given url returns a JSON body with status code 200."""
        response = self.client.get(url)

        self.assertResponseOK(response)
        self.assertIsJsonResponse(response)

    def _assert_response_not_found(self, url):
        """Assert that the given url returns a 404 status code."""
        response = self.client.get(url)

        self.assertResponseNotFound(response)

    def test_endpoint_member_full_profile(self):
        url = reverse(
            endpoints.endpoint_detail(endpoints.MEMBER_FULL_PROFILE),
            kwargs={"pk": 1423},
        )

        self._assert_response_not_found(url)

        create_sample_person(parliamentdotuk=1423)
        self._assert_response_json_ok(url)

    def test_endpoint_member_votes(self):
        url = reverse(
            endpoints.endpoint_detail(endpoints.MEMBER_VOTES),
            kwargs={"pk": 1423},
        )

        self._assert_response_not_found(url)

        create_sample_person(parliamentdotuk=1423)
        self._assert_response_json_ok(url)

    def test_endpoint_constituency(self):
        url = reverse(
            endpoints.endpoint_detail(endpoints.CONSTITUENCY),
            kwargs={"pk": 146380},
        )

        self._assert_response_not_found(url)

        create_sample_constituency(parliamentdotuk=146380)
        self._assert_response_json_ok(url)

    def test_endpoint_constituency_results(self):
        url = reverse(
            endpoints.endpoint_name(endpoints.CONSTITUENCY_RESULTS),
            kwargs={"pk": 16892, "election_id": 851},
        )

        self._assert_response_not_found(url)

        create_constituency_result_detail(
            constituency=create_sample_constituency(parliamentdotuk=16892),
            election=create_sample_election(parliamentdotuk=851),
            mp=create_sample_person(parliamentdotuk=1423),
            parliamentdotuk=5231,
        )
        self._assert_response_json_ok(url)

    def test_endpoint_party(self):
        url = reverse(
            endpoints.endpoint_detail(endpoints.PARTY),
            kwargs={"pk": 15},
        )

        self._assert_response_not_found(url)

        create_sample_party(parliamentdotuk=15)

        self._assert_response_json_ok(url)

    def test_endpoint_division_commons(self):
        url = reverse(
            endpoints.endpoint_detail(endpoints.DIVISION_COMMONS),
            kwargs={"pk": 1436},
        )

        self._assert_response_not_found(url)

        create_sample_commons_division(parliamentdotuk=1436)
        self._assert_response_json_ok(url)

    def test_endpoint_division_lords(self):
        url = reverse(
            endpoints.endpoint_detail(endpoints.DIVISION_LORDS),
            kwargs={"pk": 6367},
        )

        self._assert_response_not_found(url)

        create_sample_lords_division(parliamentdotuk=6367)
        self._assert_response_json_ok(url)

    def test_endpoint_bill(self):
        url = reverse(
            endpoints.endpoint_detail(endpoints.BILL),
            kwargs={"pk": 2741},
        )

        self._assert_response_not_found(url)

        create_sample_bill(parliamentdotuk=2741)
        self._assert_response_json_ok(url)

    def tearDown(self) -> None:
        self.delete_instances_of(
            ApiKey,
            Bill,
            BillType,
            CommonsDivision,
            Constituency,
            Election,
            ElectionType,
            LordsDivision,
            ParliamentarySession,
            Party,
            Person,
            User,
            UserToken,
            SignInServiceProvider,
        )
