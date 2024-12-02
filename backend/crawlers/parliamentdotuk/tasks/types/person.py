import re
from typing import Annotated

from pydantic import AfterValidator

from .common import StringOrNone

__all__ = [
    "PersonName",
]

"""
Titles and honorifics that are stripped from a person's name in order to get their 'core' name.
These titles are typically prepended to a full name so are easy to remove cleanly.
Some titles (e.g. Lord, Bishop) replace some portion of the name so can't easily remove them.
"""
_honorifics = [
    "dr",
    "miss",
    "mr",
    "mrs",
    "ms",
    "rt hon",
    "sir",
]
_honorifics_regex = re.compile(f"^({"|".join(_honorifics)}) ", re.IGNORECASE)


def normalize_name(raw_name: str) -> str:
    """
    Normalize a person's name.

    - Remove honorifics and titles
    - Strip any extraneous whitespace
    - Convert `Surname, Forename` format to `Forename Surname`
    """
    name = re.sub(_honorifics_regex, "", raw_name, re.IGNORECASE)

    if "," in name:
        parts = [x.strip() for x in name.split(",", maxsplit=1)]
        return " ".join(reversed(parts))
    return name


type PersonName = Annotated[StringOrNone, AfterValidator(normalize_name)]
