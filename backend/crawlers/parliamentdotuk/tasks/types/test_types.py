from datetime import date

from basetest.testcase import LocalTestCase
from pydantic import BaseModel as Schema
from util.time import tzdatetime

from . import Color, DateOrNone, DateTimeOrNone, House, List, PhoneNumber


class Obj[T](Schema):
    value: T


class TypesTests(LocalTestCase):
    def test_DateOrNone(self):
        obj = Obj[DateOrNone]

        self.assertEqual(
            obj(value="2024-03-02").value,
            date(2024, 3, 2),
        )
        self.assertEqual(
            obj(value="2024-03-02 10:42:11").value,
            date(2024, 3, 2),
        )
        self.assertIsNone(
            obj(value="blah").value,
        )

    def test_DateTimeOrNone(self):
        obj = Obj[DateTimeOrNone]

        self.assertEqual(
            obj(value="2024-03-02 10:42:11").value,
            tzdatetime(2024, 3, 2, 10, 42, 11),
        )
        self.assertIsNone(
            obj(value="blah").value,
        )

    def test_List(self):
        obj = Obj[List]

        self.assertListEqual(obj(value="a").value, ["a"])
        self.assertListEqual(obj(value=None).value, [])

    def test_House(self):
        obj = Obj[House]

        self.assertEqual(obj(value=1).value, "Commons")
        self.assertEqual(obj(value=2).value, "Lords")
        self.assertEqual(obj(value="commons").value, "Commons")
        self.assertEqual(obj(value="lords").value, "Lords")

        self.assertIsNone(obj(value=0).value)
        self.assertIsNone(obj(value="blah").value)
        self.assertIsNone(obj(value=None).value)

    def test_Color(self):
        obj = Obj[Color]

        self.assertEqual(obj(value="ff0000").value, "#ff0000")
        self.assertEqual(obj(value="#00F0F0").value, "#00f0f0")
        self.assertEqual(obj(value="invalid").value, None)
        self.assertEqual(obj(value=8).value, None)

    def test_PhoneNumber(self):
        obj = Obj[PhoneNumber]

        self.assertEqual(obj(value="0800 800150").value, "0800 800150")
        self.assertEqual(obj(value="0800 800 150").value, "0800 800150")
        self.assertEqual(obj(value="0800800150").value, "0800 800150")
        self.assertEqual(obj(value="+44800800150").value, "0800 800150")
        self.assertEqual(obj(value="016301").value, None)
        self.assertEqual(obj(value="abcde").value, None)
