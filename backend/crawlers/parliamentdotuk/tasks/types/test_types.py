from datetime import date

from basetest.testcase import SimpleTestCase
from pydantic import BaseModel as Schema
from util.time import tzdatetime

from . import (
    Color,
    DateOrNone,
    DateTimeOrNone,
    House,
    List,
    PersonName,
    PhoneNumber,
    SafeHtmlOrNone,
    StringOrNone,
)


class Obj[T](Schema):
    value: T

    def __init__(self, value, **kwargs):
        super().__init__(value=value, **kwargs)


class TypesTests(SimpleTestCase):
    def _assert_equal[T](self, _: Obj[T], expected: T, msg=None):
        if isinstance(expected, list):
            self.assertListEqual(_.value, expected, msg=msg)
        elif expected is None:
            self.assertIsNone(_.value, msg=msg)
        else:
            self.assertEqual(_.value, expected, msg=msg)

    def test_StringOrNone(self):
        _ = Obj[StringOrNone]

        self._assert_equal(_(None), None)
        self._assert_equal(_(""), "")
        self._assert_equal(_("cheese"), "cheese")
        self._assert_equal(_(" cheese"), "cheese")
        self._assert_equal(_("cheese "), "cheese")
        self._assert_equal(_("cheese  pizza "), "cheese pizza")

    def test_DateOrNone(self):
        _ = Obj[DateOrNone]

        self._assert_equal(
            _("2024-03-02"),
            date(2024, 3, 2),
        )
        self._assert_equal(
            _("2024-03-02 10:42:11"),
            date(2024, 3, 2),
        )
        self._assert_equal(_("blah"), None)

    def test_DateTimeOrNone(self):
        _ = Obj[DateTimeOrNone]

        self._assert_equal(
            _("2024-03-02 10:42:11"),
            tzdatetime(2024, 3, 2, 10, 42, 11),
        )
        self._assert_equal(_("blah"), None)

    def test_List(self):
        _ = Obj[List]

        self._assert_equal(_("a"), ["a"])
        self._assert_equal(_(None), [])

    def test_House(self):
        _ = Obj[House]

        self._assert_equal(_(1), "Commons")
        self._assert_equal(_(2), "Lords")
        self._assert_equal(_("commons"), "Commons")
        self._assert_equal(_("lords"), "Lords")

        self._assert_equal(_(0), None)
        self._assert_equal(_("blah"), None)
        self._assert_equal(_(None), None)

    def test_Color(self):
        _ = Obj[Color]

        self._assert_equal(_("ff0000"), "#ff0000")
        self._assert_equal(_("#00F0F0"), "#00f0f0")
        self._assert_equal(_("invalid"), None)
        self._assert_equal(_(8), None)

    def test_PhoneNumber(self):
        _ = Obj[PhoneNumber]

        self._assert_equal(_("0800 800150"), "0800 800150")
        self._assert_equal(_("0800 800 150"), "0800 800150")
        self._assert_equal(_("0800800150"), "0800 800150")
        self._assert_equal(_("+44800800150"), "0800 800150")
        self._assert_equal(_("016301"), None)
        self._assert_equal(_("abcde"), None)

    def test_PersonName(self):
        _ = Obj[PersonName]

        self._assert_equal(_("Sir Keir Starmer"), "Keir Starmer")
        self._assert_equal(_("Rt Hon Alistair Darling"), "Alistair Darling")
        self._assert_equal(_("Sir  Christopher Chope"), "Christopher Chope")
        self._assert_equal(_("Sirius Snape"), "Sirius Snape")
        self._assert_equal(_("Caroline   Lucas"), "Caroline Lucas")
        self._assert_equal(_("Lucas,   Caroline"), "Caroline Lucas")
        self._assert_equal(_(" Caroline Lucas "), "Caroline Lucas")
        self._assert_equal(_(" Lucas, Caroline "), "Caroline Lucas")
        self._assert_equal(_("Caroline Lucas"), "Caroline Lucas")
        self._assert_equal(_("Lucas, Caroline"), "Caroline Lucas")

    def test_SafeHtmlOrNone(self):
        _ = Obj[SafeHtmlOrNone]

        self._assert_equal(_("<p>OK</p>"), "<p>OK</p>")
        self._assert_equal(_("<div>not OK</div>"), "not OK")
        self._assert_equal(
            _("""<a href="https://example.org" data-other="blah">link edited</a>"""),
            """<a href="https://example.org" rel="noopener noreferrer nofollow">link edited</a>""",
        )

        self._assert_equal(_("<p>OK<br>Fine</p>"), "<p>OK<br>Fine</p>")
