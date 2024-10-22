from datetime import date

from basetest.testcase import LocalTestCase
from pydantic import BaseModel as Schema
from util.time import tzdatetime

from .types import CoercedDate, CoercedDateTime, CoercedList


class TypesTests(LocalTestCase):
    def test_CoercedDate(self):
        class Obj(Schema):
            date: CoercedDate

        self.assertEqual(
            Obj(date="2024-03-02").date,
            date(2024, 3, 2),
        )

    def test_CoercedDateTime(self):
        class Obj(Schema):
            datetime: CoercedDateTime

        self.assertEqual(
            Obj(datetime="2024-03-02 10:42:11").datetime,
            tzdatetime(2024, 3, 2, 10, 42, 11),
        )

    def test_CoercedList(self):
        class Obj(Schema):
            lst: CoercedList

        self.assertListEqual(Obj(lst="a").lst, ["a"])
