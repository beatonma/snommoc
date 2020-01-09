"""

"""
import datetime
import logging

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.membersdataplatform import mdp_client

log = logging.getLogger(__name__)


class MdpClientTests(LocalTestCase):
    def test__coerce_to_list(self):
        test_func = mdp_client._coerce_to_list

        self.assertEqual(test_func([]), [])
        self.assertEqual(test_func({}), [{}])
        self.assertEqual(test_func([{}]), [{}])
        self.assertEqual(test_func("a"), ["a"])
        self.assertEqual(test_func(["a"]), ["a"])

    def test__coerce_to_int(self):
        test_func = mdp_client._coerce_to_int

        self.assertEqual(test_func(123), 123)
        self.assertEqual(test_func("123"), 123)
        self.assertEqual(test_func(True), 1)
        self.assertEqual(test_func(False), 0)

        self.assertEqual(test_func(None), None)
        self.assertEqual(test_func("abc"), None)
        self.assertEqual(test_func([]), None)

    def test__coerce_to_str(self):
        test_func = mdp_client._coerce_to_str

        self.assertEqual(test_func("abc"), "abc")
        self.assertEqual(test_func(123), "123")
        self.assertEqual(test_func(True), "True")
        self.assertEqual(test_func(None), None)
        self.assertEqual(test_func([]), None)

    def test__coerce_to_date(self):
        test_func = mdp_client._coerce_to_date

        self.assertEqual(
            test_func("2017-01-02"), datetime.date(year=2017, month=1, day=2)
        )
        self.assertEqual(
            test_func("2018-02-01T00:00:00"), datetime.date(year=2018, month=2, day=1)
        )
        self.assertEqual(test_func("abcd"), None)

        self.assertEqual(
            test_func({"Year": 1997,}), datetime.date(year=1997, month=12, day=25)
        )
        self.assertEqual(
            test_func({"Year": 2001, "Month": 5, "Day": 6}),
            datetime.date(year=2001, month=5, day=6),
        )
        self.assertEqual(
            test_func({"Year": "1997",}), datetime.date(year=1997, month=12, day=25)
        )
        self.assertEqual(
            test_func({"Year": "2001", "Month": "5", "Day": "6"}),
            datetime.date(year=2001, month=5, day=6),
        )

    def test__coerce_to_boolean(self):
        test_func = mdp_client._coerce_to_boolean

        self.assertEqual(test_func("true"), True)
        self.assertEqual(test_func("True"), True)
        self.assertEqual(test_func("false"), False)
        self.assertEqual(test_func("False"), False)
        self.assertEqual(test_func(True), True)
        self.assertEqual(test_func(False), False)
        self.assertEqual(test_func(1), True)
        self.assertEqual(test_func(0), False)

        self.assertEqual(test_func(None), None)

    def test__is_xml_null(self):
        test_func = mdp_client._is_xml_null

        self.assertFalse(test_func({}))
        self.assertFalse(test_func(None))
        self.assertFalse(
            test_func(
                {
                    "@xsi:nil": "false",
                    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                }
            )
        )
        self.assertTrue(
            test_func(
                {
                    "@xsi:nil": "True",
                    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                }
            )
        )
        self.assertTrue(
            test_func(
                {
                    "@xsi:nil": "true",
                    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                }
            )
        )

    def test__get_nested_value(self):
        test_func = mdp_client._get_nested_value

        obj = {
            "simple_key": 3,
            "nested_object": {
                "nested_key": 7,
                "double_nested_object": {"double_nested_key": 11},
            },
        }

        self.assertEqual(test_func(obj, "simple_key"), 3)
        self.assertEqual(test_func(obj, "nested_object.nested_key"), 7)
        self.assertEqual(
            test_func(obj, "nested_object.double_nested_object.double_nested_key"), 11
        )
        self.assertIsNone(test_func(obj, "...."))
        self.assertIsNone(test_func(obj, ""))
        self.assertIsNone(test_func(obj, "double_nested_object.bad_key"))
