from unittest import skipUnless

from django.db import OperationalError
from django.http import HttpResponse
from django.test import TestCase
from rest_framework import status

from basetest.args import RUNTESTS_CLARGS
from util.models.generics import BaseModelMixin, get_concrete_models


class DirtyTestException(Exception):
    """Raised when a testcase fails to tidy up after itself."""

    pass


class BaseTestCase(TestCase):
    maxDiff = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delete_instances_of(
        self,
        *classList,
        check_instances: bool = RUNTESTS_CLARGS.fragile,
    ):
        """
        Delete any instances of the given model classes.
        :param check_instances: If true, check for any persisting model instances that should have been deleted.
        """
        for cls in classList:
            cls.objects.all().delete()

        if check_instances:
            self._check_cleanup()

    def _check_cleanup(self):
        """Check for any persisting instances of project database models.

        Throws DirtyTestException if any instances are found."""

        all_models = get_concrete_models(BaseModelMixin)
        for M in all_models:
            try:
                instances = M.objects.all()
                if instances.count() > 0:
                    raise DirtyTestException(
                        f"Instance(s) of model {M} still exists! {instances}"
                    )
            except OperationalError:
                # Model does not exist in the module under test
                pass

    def assertEqualIgnoreCase(self, first: str, second: str, msg=None):
        self.assertEqual(first.lower(), second.lower(), msg=msg)

    def assertLengthEquals(self, collection, expected_length: int, msg=None):
        self.assertEqual(len(collection), expected_length, msg=msg)

    def assertNoneCreated(self, model_class, msg=None):
        self.assertEqual(model_class.objects.all().count(), 0, msg=msg)

    def assertQuerysetSize(self, queryset, expected_length: int, msg=None):
        self.assertLengthEquals(queryset.all(), expected_length, msg=msg)

    def assertContentsEqual(self, first: list, second: list, msg=None):
        """Ensure the lists have the same items, ignoring the order of appearance."""
        differences = []

        if len(first) != len(second):
            raise AssertionError(
                f"assertContentsEqual failed: Lists have different lengths [{len(first)} != {len(second)}]"
            )

        def appearances(item, lst) -> int:
            return len(list(filter(lambda x: x == item, lst)))

        for item in set(first + second):
            in_first = appearances(item, first)
            in_second = appearances(item, second)
            if in_first != in_second:
                differences.append((item, in_first, in_second))

        if differences:
            print(f"differences: {differences}")
            message = "\n".join(
                [
                    f"in_first={in_first} in_second={in_second} item={item}"
                    for (item, in_first, in_second) in differences
                ]
            )
            raise AssertionError(f"assertContentsEqual failed [{msg or ''}]: {message}")
        else:
            print(f"Lists have same items {first}, {second}")


class LocalTestCalledNetwork(Exception):
    """
    LocalTestCase implementations should never make network calls!
    """

    pass


class LocalTestCase(BaseTestCase):
    """Tests that use only local data - no external network calls!

    Always run when runtests.py is run.
    """

    def _catch_network_call(self, *args, **kwargs):
        raise LocalTestCalledNetwork(f"Illegal network call: {args} [{kwargs}]")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        import crawlers.network

        crawlers.network.get_json = lambda *args, **kwargs: self._catch_network_call(
            *args, **kwargs
        )


class LocalApiTestCase(LocalTestCase):
    def assertResponseOK(self, response: HttpResponse):
        self.assertResponseCode(response, status.HTTP_200_OK)

    def assertResponseNotFound(self, response: HttpResponse):
        self.assertResponseCode(response, status.HTTP_404_NOT_FOUND, msg=f"{response}")

    def assertResponseCode(self, response: HttpResponse, expected_code: int, msg=""):
        self.assertEqual(
            response.status_code,
            expected_code,
            msg=f"Expected status={expected_code} {msg}",
        )

    def assertIsJsonResponse(self, response: HttpResponse):
        self.assertEqual(response["Content-Type"], "application/json")


@skipUnless(RUNTESTS_CLARGS.network, reason="Network calls disabled by default")
class NetworkTestCase(BaseTestCase):
    """Tests that interact a remote server.

    Only run when specifically enabled via command line `-network` flag::
        runtests.py -network
    """

    pass
