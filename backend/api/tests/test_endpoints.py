from typing import Callable

from api import permissions, status
from basetest.test_util import create_sample_user
from basetest.testcase import LocalTestCase
from django.urls import reverse
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


class LocalApiTestCase(LocalTestCase):
    def setUp(self) -> None:
        self.user_with_permission = create_sample_user(username="endpoints")
        permissions.grant_read_snommoc_api(self.user_with_permission)

    def assertResponseOK(self, url: str):
        self.assertResponseCode(url, status.HTTP_200_OK, msg=url)

    def assertResponseNotFound(self, url: str):
        self.assertResponseCode(url, status.HTTP_404_NOT_FOUND, msg=url)

    def assertResponseUnauthorized(self, url: str):
        self.assertResponseCode(url, status.HTTP_401_UNAUTHORIZED, msg=url)

    def assertResponseCode(self, url: str, expected_code: int, msg=""):
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            expected_code,
            msg=f"Expected status={expected_code} {msg}",
        )

    @staticmethod
    def reverse(url_name: str, *args, **kwargs):
        return reverse(f"api-2.0:{url_name}", args=args, kwargs=kwargs)


def list_testcase(label: str, *, list_url: str, create_object: Callable):
    """Test responses for an item list view, with and without auth."""

    class _TestCase(LocalApiTestCase):
        def test_list_without_auth(self):
            self.client.logout()
            self.assertResponseUnauthorized(list_url)
            create_object()
            self.assertResponseUnauthorized(list_url)

        def test_list_with_auth(self):
            self.client.force_login(self.user_with_permission)
            self.assertResponseOK(list_url)
            create_object()
            self.assertResponseOK(list_url)

        test_list_with_auth.__name__ = f"{label}_list_with_auth"
        test_list_without_auth.__name__ = f"{label}_list_without_auth"

    _TestCase.__name__ = f"{label}_ListTestCase"
    return _TestCase


def detail_testcase(label: str, *, detail_url: str, create_object: Callable):
    class _TestCase(LocalApiTestCase):
        """Test responses for an item detail view, with and without auth."""

        def test_detail_without_auth(self):
            self.client.logout()
            self.assertResponseUnauthorized(detail_url)
            create_object()
            self.assertResponseUnauthorized(detail_url)

        def test_detail_with_auth(self):
            self.client.force_login(self.user_with_permission)
            self.assertResponseNotFound(detail_url)
            create_object()
            self.assertResponseOK(detail_url)

        test_detail_with_auth.__name__ = f"{label}_detail_with_auth"
        test_detail_without_auth.__name__ = f"{label}_detail_without_auth"

    _TestCase.__name__ = f"{label}_DetailTestCase"
    return _TestCase


def list_detail_testcase(
    label: str, *, list_url: str, detail_url: str, create_object: Callable
):
    class _TestCase(
        list_testcase(label, list_url=list_url, create_object=create_object),
        detail_testcase(label, detail_url=detail_url, create_object=create_object),
    ):
        pass

    _TestCase.__name__ = f"{label}_ListDetailTestCase"
    return _TestCase


class MembersTests(
    list_detail_testcase(
        "MembersTests",
        list_url=LocalApiTestCase.reverse("members"),
        detail_url=LocalApiTestCase.reverse("member", 1423),
        create_object=lambda: create_sample_person(1423),
    )
):
    pass


class MemberVotesTests(
    detail_testcase(
        "MemberVotesTests",
        detail_url=LocalApiTestCase.reverse("member_votes", parliamentdotuk=1423),
        create_object=lambda: create_sample_person(1423),
    )
):
    pass


class MemberCareerTests(
    detail_testcase(
        "MemberHistoryTests",
        detail_url=LocalApiTestCase.reverse("member_career", parliamentdotuk=1423),
        create_object=lambda: create_sample_person(1423),
    )
):
    pass


class ConstituencyResultsTests(
    detail_testcase(
        "ConstituencyResultsTests",
        detail_url=LocalApiTestCase.reverse(
            "constituency_election_result",
            constituency_parliamentdotuk=16892,
            election_parliamentdotuk=851,
        ),
        create_object=lambda: create_constituency_result_detail(
            constituency=create_sample_constituency(parliamentdotuk=16892),
            election=create_sample_election(parliamentdotuk=851),
            mp=create_sample_person(parliamentdotuk=1423),
        ),
    )
):
    pass


class ConstituencyTests(
    list_detail_testcase(
        "ConstituencyTests",
        list_url=LocalApiTestCase.reverse("constituencies"),
        detail_url=LocalApiTestCase.reverse("constituency", parliamentdotuk=146380),
        create_object=lambda: create_sample_constituency(parliamentdotuk=146380),
    )
):
    pass


class PartyTests(
    list_detail_testcase(
        "PartyTests",
        list_url=LocalApiTestCase.reverse("parties"),
        detail_url=LocalApiTestCase.reverse("party", parliamentdotuk=15),
        create_object=lambda: create_sample_party(parliamentdotuk=15),
    )
):
    pass


class CommonsDivisionTests(
    list_detail_testcase(
        "CommonsDivisionTests",
        list_url=LocalApiTestCase.reverse("commons_divisions"),
        detail_url=LocalApiTestCase.reverse("commons_division", parliamentdotuk=1436),
        create_object=lambda: create_sample_commons_division(parliamentdotuk=1436),
    )
):
    pass


class LordsDivisionTests(
    list_detail_testcase(
        "LordsDivisionTests",
        list_url=LocalApiTestCase.reverse("lords_divisions"),
        detail_url=LocalApiTestCase.reverse("lords_division", parliamentdotuk=6367),
        create_object=lambda: create_sample_lords_division(parliamentdotuk=6367),
    )
):
    pass


class BillsTests(
    list_detail_testcase(
        "BillsTests",
        list_url=LocalApiTestCase.reverse("bills"),
        detail_url=LocalApiTestCase.reverse("bill", parliamentdotuk=2741),
        create_object=lambda: create_sample_bill(parliamentdotuk=2741),
    )
):
    pass
