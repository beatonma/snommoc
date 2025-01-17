from basetest.testcase import DatabaseTestCase
from crawlers.parliamentdotuk.tasks.openapi.members import member_detail, schema
from crawlers.parliamentdotuk.tasks.openapi.members.member_detail import (
    finalize_members_update,
)
from repository.models import House, RegisteredInterestCategory
from repository.tests.data.create import create_houses


class DataCorrectionTests(DatabaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        create_houses()

        # Structure: (name, house_name, api_sort_order)
        data = (
            ("1. Employment and earnings", "Commons", 0),
            (
                "2. (a) Support linked to an MP but received by a local party organisation or indirectly via a central party organisation",
                "Commons",
                0,
            ),
            (
                "6. Land and property portfolio with a value over £100,000 and where indicated, the portfolio provides a rental income of over £10,000 a year",
                "Commons",
                1,
            ),
            (
                "9. Family members employed and paid from parliamentary expenses",
                "Commons",
                1,
            ),
            ("2. (b) Any other support not included in Category 2(a)", "Commons", 2),
            ("3. Gifts, benefits and hospitality from UK sources", "Commons", 2),
            ("5. Gifts and benefits from sources outside the UK", "Commons", 2),
            (
                "10. Family members engaged in lobbying the public sector on behalf of a third party or client",
                "Commons",
                3,
            ),
            ("4. Visits outside the UK", "Commons", 4),
            ("7. (i) Shareholdings: over 15% of issued share capital", "Commons", 4),
            ("7. (ii) Other shareholdings, valued at more than £70,000", "Commons", 4),
            ("8. Miscellaneous", "Commons", 5),
            ("Nil", "Lords", 0),
            ("1: Directorships", "Lords", 100),
            ("2: Remunerated employment, office, profession etc.", "Lords", 200),
            ("3: Person with significant control of a company (PSC)", "Lords", 300),
            ("4: Shareholdings (a)", "Lords", 400),
            ("4: Shareholdings (b)", "Lords", 410),
            ("4: Shareholdings (c)", "Lords", 420),
            ("5: Land and property", "Lords", 500),
            ("6: Sponsorship", "Lords", 600),
            ("7: Overseas visits", "Lords", 700),
            ("8: Gifts, benefits and hospitality", "Lords", 800),
            ("9: Miscellaneous financial interests", "Lords", 900),
            ("10: Non-financial interests (a)", "Lords", 1000),
            ("10: Non-financial interests (b)", "Lords", 1010),
            ("10: Non-financial interests (c)", "Lords", 1020),
            ("10: Non-financial interests (d)", "Lords", 1030),
            ("10: Non-financial interests (e)", "Lords", 1040),
        )
        for name, house, sort_order in data:
            member_detail._get_registered_interest_category(
                House.objects.get(name=house),
                schema.RegisteredInterestCategory.model_validate(
                    {"name": name, "sortOrder": sort_order, "interests": []}
                ),
            )

    def test_registeredinterestcategory_sortorder_is_correct(self):
        finalize_members_update()

        # Default ordering uses sort_order which should be correct after
        # calling finalize_members_update()
        categories = RegisteredInterestCategory.objects.all()
        house_categories = list(
            categories.filter(house=House.objects.commons()).values_list(
                "name", flat=True
            )
        )
        lords_categories = list(
            categories.filter(house=House.objects.lords()).values_list(
                "name", flat=True
            )
        )

        self.assertListEqual(
            house_categories,
            [
                "1. Employment and earnings",
                "2. (a) Support linked to an MP but received by a local party organisation or indirectly via a central party organisation",
                "2. (b) Any other support not included in Category 2(a)",
                "3. Gifts, benefits and hospitality from UK sources",
                "4. Visits outside the UK",
                "5. Gifts and benefits from sources outside the UK",
                "6. Land and property portfolio with a value over £100,000 and where indicated, the portfolio provides a rental income of over £10,000 a year",
                "7. (i) Shareholdings: over 15% of issued share capital",
                "7. (ii) Other shareholdings, valued at more than £70,000",
                "8. Miscellaneous",
                "9. Family members employed and paid from parliamentary expenses",
                "10. Family members engaged in lobbying the public sector on behalf of a third party or client",
            ],
        )

        self.assertListEqual(
            lords_categories,
            [
                "Nil",
                "1: Directorships",
                "2: Remunerated employment, office, profession etc.",
                "3: Person with significant control of a company (PSC)",
                "4: Shareholdings (a)",
                "4: Shareholdings (b)",
                "4: Shareholdings (c)",
                "5: Land and property",
                "6: Sponsorship",
                "7: Overseas visits",
                "8: Gifts, benefits and hospitality",
                "9: Miscellaneous financial interests",
                "10: Non-financial interests (a)",
                "10: Non-financial interests (b)",
                "10: Non-financial interests (c)",
                "10: Non-financial interests (d)",
                "10: Non-financial interests (e)",
            ],
        )
