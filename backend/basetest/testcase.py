import sys
from datetime import datetime
from io import StringIO
from unittest import skipIf
from unittest.mock import Mock, patch

import django.core.management
import pytest
from django.http import HttpResponse
from django.test import TestCase
from rest_framework import status
from util.time import coerce_timezone


class DirtyTestException(Exception):
    """Raised when a testcase fails to tidy up after itself."""

    pass


class BaseTestCase(TestCase):
    maxDiff = None

    def delete_instances_of(
        self,
        *classList,
    ):
        """
        Delete any instances of the given model classes.
        :param check_instances: If true, check for any persisting model instances that should have been deleted.
        """
        for cls in classList:
            cls.objects.all().delete()

    def assertEqualIgnoreCase(self, first: str, second: str, msg=None):
        self.assertEqual(first.lower(), second.lower(), msg=msg)

    def assertLengthEquals(self, collection, expected_length: int, msg=None):
        self.assertEqual(len(collection), expected_length, msg=msg)

    def assertDateTimeEqual(self, actual: datetime, expected: datetime, msg=None):
        self.assertEqual(actual, coerce_timezone(expected), msg=msg)

    def assertNoneCreated(self, model_class, msg=None):
        self.assertEqual(model_class.objects.all().count(), 0, msg=msg)

    def assertQuerysetSize(self, queryset, expected_length: int, msg=None):
        self.assertLengthEquals(queryset.all(), expected_length, msg=msg)

    def assertContentsEqual(self, first: list, second: list, msg=None):
        """Ensure the lists have the same items, ignoring the order of appearance."""
        differences = []

        if len(first) != len(second):
            raise AssertionError(
                "assertContentsEqual failed: Lists have different lengths"
                f" [{len(first)} != {len(second)}]"
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

    Local tests run by default but are disabled when `-network` command line flag is passsed to runtests.
    """

    pass


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


class LocalManagementTestCase(LocalTestCase):
    """Tests for manage.py commands."""

    command = None

    def call_command(self, *args, sync: bool = True, **kwargs) -> str:
        from django.core.management import CommandError, call_command

        if self.command is None:
            raise NotImplementedError("LocalManagementTestCase must set self.command!")

        print(
            f"Running `manage.py {self.command} args={args} kwargs={kwargs}"
            f" {'-sync' if sync else ''}`"
        )

        out = StringIO()
        try:
            # Bypass @lru_cache decorator on get_commands to make sure we can
            # find commands for the current state of settings.INSTALLED_APPS.
            with patch.object(
                django.core.management,
                "get_commands",
                side_effect=Mock(wraps=django.core.management.get_commands.__wrapped__),
            ):
                call_command(
                    self.command,
                    *args,
                    stdout=out,
                    stderr=StringIO(),
                    sync=sync,
                    **kwargs,
                )

        except CommandError as e:
            print(e)
            raise e

        return out.getvalue()


@pytest.mark.skipif("not config.getoption('network')")
@skipIf(
    "manage.py" in sys.argv,
    reason="Use `pytest --network` to run tests from NetworkTestCase.",
)
class NetworkTestCase(BaseTestCase):
    """Tests that interact a remote server.

    Network tasks are disabled by default but can be executed by passing the `-network` command line flag to runtests.
    """

    pass
