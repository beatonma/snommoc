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

        self.assertEquals(test_func([]), [])
        self.assertEquals(test_func({}), [{}])
        self.assertEquals(test_func([{}]), [{}])
        self.assertEquals(test_func('a'), ['a'])
        self.assertEquals(test_func(['a']), ['a'])

    def test__coerce_to_int(self):
        test_func = mdp_client._coerce_to_int

        self.assertEquals(test_func(123), 123)
        self.assertEquals(test_func('123'), 123)
        self.assertEquals(test_func(True), 1)
        self.assertEquals(test_func(False), 0)

        self.assertEquals(test_func(None), None)
        self.assertEquals(test_func('abc'), None)
        self.assertEquals(test_func([]), None)

    def test__coerce_to_str(self):
        test_func = mdp_client._coerce_to_str

        self.assertEquals(test_func('abc'), 'abc')
        self.assertEquals(test_func(123), '123')
        self.assertEquals(test_func(True), 'True')
        self.assertEquals(test_func(None), None)
        self.assertEquals(test_func([]), None)

    def test__coerce_to_date(self):
        test_func = mdp_client._coerce_to_date

        self.assertEquals(test_func('2017-01-02'), datetime.date(year=2017, month=1, day=2))
        self.assertEquals(test_func('2018-02-01T00:00:00'), datetime.date(year=2018, month=2, day=1))
        self.assertEquals(test_func('abcd'), None)

    def test__coerce_to_boolean(self):
        test_func = mdp_client._coerce_to_boolean

        self.assertEquals(test_func('true'), True)
        self.assertEquals(test_func('True'), True)
        self.assertEquals(test_func('false'), False)
        self.assertEquals(test_func('False'), False)
        self.assertEquals(test_func(True), True)
        self.assertEquals(test_func(False), False)
        self.assertEquals(test_func(1), True)
        self.assertEquals(test_func(0), False)

        self.assertEquals(test_func(None), None)

    def test__is_xml_null(self):
        test_func = mdp_client._is_xml_null

        self.assertFalse(test_func({}))
        self.assertFalse(test_func(None))
        self.assertFalse(
            test_func({
                '@xsi:nil': 'false',
                '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'
            }))
        self.assertTrue(
            test_func({
                '@xsi:nil': 'True',
                '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'
            }))
        self.assertTrue(
            test_func({
                '@xsi:nil': 'true',
                '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'
            }))

    def test__get_nested_value(self):
        test_func = mdp_client._get_nested_value

        obj = {
            'simple_key': 3,
            'nested_object': {
                'nested_key': 7,
                'double_nested_object': {
                    'double_nested_key': 11
                }
            }
        }

        self.assertEquals(test_func(obj, 'simple_key'), 3)
        self.assertEquals(test_func(obj, 'nested_object.nested_key'), 7)
        self.assertEquals(test_func(obj, 'nested_object.double_nested_object.double_nested_key'), 11)
        self.assertIsNone(test_func(obj, '....'))
        self.assertIsNone(test_func(obj, ''))
        self.assertIsNone(test_func(obj, 'double_nested_object.bad_key'))
