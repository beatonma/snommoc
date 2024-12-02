from basetest.testcase import SimpleTestCase
from util.strings import ellipsise


class StringUtilTests(SimpleTestCase):
    def test_ellipsise(self):
        short = "a" * 25  # Should be unchanged
        at_limit = "a" * 32  # Should be unchanged
        long = "a" * 33  # Should be trimmed with ellipsis

        self.assertEqual(ellipsise(short), short)
        self.assertEqual(ellipsise(at_limit), at_limit)

        self.assertEqual(len(ellipsise(long)), 32)
        self.assertEqual(ellipsise(long), f"{'a' * 31}…")
