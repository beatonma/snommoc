import re
from collections import OrderedDict
from datetime import date, datetime
from typing import Self

from crawlers.parliamentdotuk.tasks.types import (
    DateTimeOrNone,
    List,
    StringOrNone,
    StringOrNoneKeepBreaks,
    field,
)
from pydantic import BaseModel as Schema
from pydantic import model_validator


class RegisteredInterest(Schema):
    interest_id: int = field("id")
    description: StringOrNoneKeepBreaks = field("interest")
    description_data: dict = None
    created_at: DateTimeOrNone = field("createdWhen")
    last_amended_at: DateTimeOrNone = field("lastAmendedWhen")
    deleted_at: DateTimeOrNone = field("deletedWhen")
    is_correction: bool = field("isCorrection")
    child_interests: List[Self] = field("childInterests")

    @model_validator(mode="after")
    @classmethod
    def validate_description_data(cls, obj: Self):
        """Parse as many known fields from the description as possible and
        store the serialized result for frontend API use."""
        obj.description_data = _parse_description(obj.description).model_dump(
            mode="json"
        )

        return obj


class RegisteredInterestCategory(Schema):
    sort_order: int = field("sortOrder")
    name: StringOrNone
    codename_major: int
    codename_minor: StringOrNone
    interests: List[RegisteredInterest]

    @model_validator(mode="before")
    @classmethod
    def validate_codename(cls, obj):
        """Extract codename values from category name.

        Codename values are used for sorting categories correctly.
        e.g. "2. (b) Any other support not included in Category 2(a)" should
             yield codename_major=2, codename_minor="b"
        """
        name = obj["name"].removeprefix("Category ")

        match = re.match(
            r"^(?P<major>\d+)[:.] (\((?P<minor_start>[a-z]+)\) )?(?P<name>.*?)( \((?P<minor_end>[a-z]+)\))?$",
            name,
        )
        groups = match.groupdict() if match else {}
        obj["codename_major"] = int(groups.get("major", 0))
        obj["codename_minor"] = groups.get("minor_start") or groups.get("minor_end")
        obj["name"] = re.sub(r"(^\d+)(:)", r"\1.", name)

        return obj


_registration_date_keys = {
    "Date accepted": "Accepted",
    "Date received": "Received",
    "Registered": None,
    "Updated": None,
}
_start_date_keys = {
    "Date interest arose": None,
}
_end_date_keys = {
    "Date interest ended": None,
    "End date": None,
}
"""Replacements for lengthy entries in interest description."""
_description_keys = {
    **_registration_date_keys,
    **_start_date_keys,
    **_end_date_keys,
    "ACOBA consulted": None,
    "Additional information": None,
    "Address of donor": "Donor address",
    "Amount of donation or nature and value if donation in kind": "Donation value",
    "Completed or provided on": None,
    "Dates of visit": "Dates",
    "Destination of visit": "Destination",
    "Donated to": None,
    "Donor status": None,
    "Estimate of the probable value (or amount of any donation)": "Donation value",
    "From": None,
    "Held jointly with or on behalf of": None,
    "Hours": None,
    "Interest held": None,
    "Location": None,
    "Name of company or organisation": "Organisation",
    "Name of donor": "Donor",
    "Name of employer": "Employer",
    "Name": None,
    "Nature of business": None,
    "Number of properties": None,
    "Ownership details": None,
    "Paid directly to": None,
    "Payer": None,
    "Payment expected": None,
    "Payment": None,
    "Purpose of visit": None,
    "Relationship": None,
    "Remuneration": None,
    "Rental income details": None,
    "Rental income": None,
    "Role": None,
    "Role, work or services": None,
    "Type of land/property": None,
    "Ultimate payer": None,
    "Unpaid Directorship at": "Unpaid Directorship",
    "Unpaid Directorship of": "Unpaid Directorship",
    "Until": None,
    "Work or services": None,
    "Working pattern": None,
}


class ParsedInterestDescription(Schema):
    """The result of parsing the raw string of a RegisteredInterest description.

    Description contains a mixture of semi-structured and arbitrary content."""

    """key-value pairs for display in a table"""
    table: list[tuple[str, str | int | date]]

    """Non-keyed descriptions"""
    additional_values: list[str]

    """Start date of period during which the interest is/was active, if available."""
    start: str | None

    """Start date of period during which the interest is/was active, if available."""
    end: str | None

    """key-value pairs for display in a table
    Dates related to the registration of this interest.
    There can be many of these dates and some of these appear to duplicate one 
    another, although they often have different values, and it's not clear which
    should take priority over others, if any."""
    registration_dates: list[tuple[str, str | date]]


def _parse_description(description: str) -> ParsedInterestDescription:
    table = OrderedDict()
    registration_dates = OrderedDict()
    additional_values: list[str] = []
    start: str | None = None
    end: str | None = None

    for line in description.split("\n"):
        line = line.removesuffix(".")
        colon_count = line.count(":")

        if colon_count == 1:
            # simple key-value pair
            k, v = line.split(":")
            if k in _registration_date_keys:
                _append_clean(registration_dates, k, v)
            elif k in _start_date_keys:
                start = v
            elif k in _end_date_keys:
                end = v
            else:
                _append_clean(table, k, v)
            continue

        if colon_count == 0:
            # Remove wrapping parentheses.
            if line.startswith("("):
                line = line.removeprefix("(").removesuffix(")")

            # Parse registration dates
            if match := re.match(
                r"(?P<k1>Registered) (?P<v1>\d{1,2} \w+ \d{4})(; (?P<k2>\w+) (?P<v2>\d{1,2} \w+ \d{4}))?",
                line,
            ):
                _append_clean(registration_dates, match.group("k1"), match.group("v1"))
                if k2 := match.group("k2"):
                    _append_clean(registration_dates, k2, match.group("v2"))

                continue

            # Any unhandled values
            additional_values.append(line)
            continue

        # Check special cases for lines with multiple values
        if match := re.match(
            r"(?P<k1>From): (?P<v1>.*?)\. (?P<k2>Until): (?P<v2>.*)",
            line,
        ):
            start = match.group("v1")
            end = match.group("v2")
            continue

        if match := re.match(
            r"(?P<k1>Received on): (?P<v1>.*?)\. (?P<k2>Hours): (?P<v2>.*)",
            line,
        ):
            _append_clean(table, match.group("k1"), match.group("v1"))
            _append_clean(table, match.group("k2"), match.group("v2"))
            continue

    return ParsedInterestDescription.model_validate(
        {
            "table": table.items(),
            "additional_values": additional_values,
            "registration_dates": _clean_dates(registration_dates).items(),
            "start": start,
            "end": end,
        }
    )


def _clean_dates(dates: OrderedDict) -> OrderedDict:
    """Remove dates which are functional duplicates of another."""

    def _merge(k1: str, k2: str):
        if k1 in dates and k2 in dates and dates[k1] == dates[k2]:
            del dates[k2]

    _merge("Accepted", "Received")
    _merge("Registered", "Accepted")

    return dates


def _clean(key: str, value: str) -> tuple[str, str | None]:
    """Coerce both parts to expected format:
    - Replace key with preferred key from _description_keys.
    - Capitalise first letter
    - Convert string dates to date objects
    """
    key = _description_keys.get(key) or key

    value = re.sub(r"^[\s.]+|[\s.]+$", "", value)
    if not value:
        return key, None

    key = key[0].upper() + key[1:]
    value = value[0].upper() + value[1:]

    try:
        value = datetime.strptime(value, "%d %B %Y").date()
    except ValueError:
        pass

    return key, value


def _append_clean(obj: dict, key: str, value: str | int):
    key, value = _clean(key, value)
    if value:
        obj[key] = value
