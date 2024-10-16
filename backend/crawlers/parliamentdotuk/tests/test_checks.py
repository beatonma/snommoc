from basetest.testcase import LocalTestCase
from crawlers.parliamentdotuk.tasks.util.checks import (
    _has_required_fields,
    MissingFieldException,
    check_required_fields,
)


class CheckTests(LocalTestCase):
    """"""

    def test_has_required_fields_is_correct(self):
        data = {
            "a": 3,
            "b": 7,
            "c": 11,
        }

        self.assertTrue(_has_required_fields(data, ["a", "b", "c"]))
        self.assertTrue(_has_required_fields(data, ["a", "b"]))

        self.assertFalse(_has_required_fields(data, ["a", "b", "d"]))
        self.assertFalse(_has_required_fields(data, ["a", "b", "c", "d"]))

    def test_check_required_fields_should_throw_MissingFieldException_when_field_missing(
        self,
    ):
        data = {
            "a": 31,
            "b": 23,
            "c": 13,
        }

        check_required_fields(data, "a", "b", "c")

        self.assertRaises(
            MissingFieldException, check_required_fields, data, "a", "b", "c", "d"
        )
        self.assertRaises(MissingFieldException, check_required_fields, data, "c", "d")
        self.assertRaises(
            MissingFieldException, check_required_fields, data, "x", "y", "z"
        )
