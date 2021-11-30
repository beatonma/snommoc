from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.membersdataplatform import mdp_client


class MdpClientTests(LocalTestCase):
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
