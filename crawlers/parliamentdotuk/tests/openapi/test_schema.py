from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.openapi.schema import DivisionSchema
from crawlers.parliamentdotuk.tests.openapi.data_lordsdivision import LORDS_DIVISION


class SchemaTestCase(LocalTestCase):
    def test_lordsdivision_schema(self):
        schema = DivisionSchema(**LORDS_DIVISION)

        self.assertEqual(2613, schema.divisionId)
        self.assertEqual(2, len(schema.contents))

        self.assertEqual("Lord Pendry", schema.contents[0].name)
