from datetime import date

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda.schema import types
from crawlers.parliamentdotuk.tasks.lda.schema.division import CommonsDivision
from pydantic import BaseModel

from . import testdata


class TestSchema(LocalTestCase):
    def test_date(self):
        class Schema(BaseModel):
            date: types.NestedDate

        schema = Schema(
            **{
                "data": "string",
                "date": {
                    "_value": "2024-05-24",
                    "_datatype": "dateTime",
                },
            }
        )

        self.assertEqual(schema.date, date(2024, 5, 24))

    def test_division(self):
        division = CommonsDivision.model_validate_json(testdata.DIVISION)

        self.assertEqual(division.parliamentdotuk, 1720037)
        self.assertEqual(division.date, date(2024, 5, 23))
        self.assertEqual(division.title, "Finance (No. 2) Bill: Third Reading")
        self.assertEqual(division.uin, "CD:2024-05-23:1823")

        vote = division.votes[0]
        self.assertEqual(vote.member_parliamentdotuk, 3950)
        self.assertEqual(vote.type, "AyeVote")
