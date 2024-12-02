from basetest.testcase import SimpleTestCase
from social.validation.username import is_username_blocked


class ValidationTestCase(SimpleTestCase):
    def test_username_blocking(self):
        self.assertFalse(is_username_blocked("name", [], []))
        self.assertFalse(is_username_blocked("NAME", ["name65"], []))
        self.assertFalse(is_username_blocked("name", ["NAME65"], []))
        self.assertTrue(is_username_blocked("name", ["name"], []))
        self.assertTrue(is_username_blocked("NAME", ["name"], []))
        self.assertTrue(is_username_blocked("name", [], ["am"]))
        self.assertTrue(is_username_blocked("NAME65", [], ["am"]))
