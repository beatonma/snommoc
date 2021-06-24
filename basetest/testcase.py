import logging
from unittest import (
    skipUnless,
)

from django.test import TestCase

from basetest.args import RUNTESTS_CLARGS


log = logging.getLogger(__name__)


class BaseTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def delete_instances_of(self, *classList):
        for cls in classList:
            try:
                cls.objects.all().delete()
            except Exception as e:
                log.warning(e)

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


class LocalTestCase(BaseTestCase):
    """Tests that use only local data - no external network calls!

    Always run when runtests.py is run.
    """

    pass


@skipUnless(RUNTESTS_CLARGS.network, reason="Network calls disabled by default")
class NetworkTestCase(BaseTestCase):
    """Tests that interact a remote server.

    Only run when specifically enabled via command line `-network` flag::
        runtests.py -network
    """

    pass
