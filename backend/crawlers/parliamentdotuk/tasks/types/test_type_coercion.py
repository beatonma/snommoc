import datetime

from basetest.testcase import SimpleTestCase
from crawlers.parliamentdotuk.tasks.types.coercion import (
    coerce_to_date,
    coerce_to_datetime,
    coerce_to_int,
    coerce_to_list,
    coerce_to_str,
)


class TypeCoercionTests(SimpleTestCase):
    def test_coerce_to_list(self):
        test_func = coerce_to_list

        self.assertEqual(test_func([]), [])
        self.assertEqual(test_func({}), [{}])
        self.assertEqual(test_func([{}]), [{}])
        self.assertEqual(test_func("a"), ["a"])
        self.assertEqual(test_func(["a"]), ["a"])

    def test_coerce_to_int(self):
        test_func = coerce_to_int

        self.assertEqual(test_func(123), 123)
        self.assertEqual(test_func("123"), 123)
        self.assertEqual(test_func(True), 1)
        self.assertEqual(test_func(False), 0)

        self.assertEqual(test_func(None), None)
        self.assertEqual(test_func("abc"), None)
        self.assertEqual(test_func([]), None)

    def test_coerce_to_str(self):
        test_func = coerce_to_str

        self.assertEqual(test_func("abc"), "abc")
        self.assertEqual(test_func(""), "")
        self.assertEqual(test_func(123), "123")
        self.assertEqual(test_func(True), "True")
        self.assertEqual(test_func(None), None)

    def test_coerce_to_date(self):
        test_func = coerce_to_date

        self.assertEqual(
            test_func("2017-01-02"), datetime.date(year=2017, month=1, day=2)
        )
        self.assertEqual(
            test_func("2018-02-01T00:00:00"), datetime.date(year=2018, month=2, day=1)
        )
        self.assertEqual(test_func("abcd"), None)

        self.assertEqual(
            test_func(
                {
                    "Year": 1997,
                }
            ),
            datetime.date(year=1997, month=12, day=25),
        )
        self.assertEqual(
            test_func({"Year": 2001, "Month": 5, "Day": 6}),
            datetime.date(year=2001, month=5, day=6),
        )
        self.assertEqual(
            test_func(
                {
                    "Year": "1997",
                }
            ),
            datetime.date(year=1997, month=12, day=25),
        )
        self.assertEqual(
            test_func({"Year": "2001", "Month": "5", "Day": "6"}),
            datetime.date(year=2001, month=5, day=6),
        )

    def test_coerce_to_datetime(self):
        test_func = coerce_to_datetime
        self.assertEqual(
            test_func("2021-11-22T11:45:21.783Z"),
            datetime.datetime(
                year=2021,
                month=11,
                day=22,
                hour=11,
                minute=45,
                second=21,
                microsecond=783000,
                tzinfo=datetime.timezone.utc,
            ),
        )
