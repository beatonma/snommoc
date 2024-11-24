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
