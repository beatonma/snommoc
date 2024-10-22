from datetime import date

from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.lda.schema import Page, types
from crawlers.parliamentdotuk.tasks.lda.schema.constituency import Constituency
from crawlers.parliamentdotuk.tasks.lda.schema.division import CommonsDivision
from pydantic import BaseModel

from . import testdata


class TestSchema(LocalTestCase):
    def test_page(self):
        page = Page[Constituency].model_validate_json(testdata.PAGE)

        self.assertEqual(page.items[0].parliamentdotuk, 146744)
        self.assertEqual(len(page.items), 7)
        self.assertTrue(page.prev_page_url.endswith("page=386"))
        self.assertEqual(page.next_page_url, None)

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
