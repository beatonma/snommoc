from basetest.testcase import LocalTestCase


class AssertionTests(LocalTestCase):
    """Ensure that custom assertions defined in BaseTestCase work correctly."""

    def assertRaisesAssertion(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except AssertionError:
            return

        raise AssertionError(
            f"AssertionError was not raised by {func} with args={args}, kwargs={kwargs}"
        )

    def test_assertRaisesAssertion(self):
        """This is a bit meta - check that assertRaisesAssertion is correct"""

        def _throws():
            raise AssertionError("_throw()")

        def _does_not_throw():
            pass

        self.assertRaisesAssertion(
            _throws,
        )

        try:
            self.assertRaisesAssertion(
                _does_not_throw,
            )
            raise Exception(
                "assertRaisesAssertion(_does_not_throw) should have raised an AssertionError!"
            )
        except AssertionError as e:
            assert "was not raised by" in str(e)

    def test_assertContentsEqual(self):
        self.assertContentsEqual([], [])
        self.assertContentsEqual([1, 1, 1, 1], [1, 1, 1, 1])
        self.assertContentsEqual([1, 2, 3], [1, 2, 3])
        self.assertContentsEqual([1, 2, 3], [2, 3, 1])
        self.assertContentsEqual([1, 2, 3], [3, 2, 1])

        # Check that duplicated items are handled correctly
        self.assertContentsEqual([1, 2, 3, 3], [3, 2, 1, 3])
        self.assertContentsEqual([1, 2, 3, 3, 9, 9, 8], [8, 3, 9, 2, 1, 9, 3])

        self.assertRaisesAssertion(
            self.assertContentsEqual,
            [1, 2, 3],
            [1, 2, 3, 4],
        )

        # Different number of twos and threes
        self.assertRaisesAssertion(
            self.assertContentsEqual,
            [1, 2, 3, 3],
            [1, 2, 2, 3],
        )

        self.assertRaisesAssertion(
            self.assertContentsEqual,
            [1, 2, 3],
            [1, 2, 4],
        )
