import re

"""
Titles and honorifics that may need to be stripped from a name when trying to resolve a Person.

These are typically prepended to a full name. Other honorifics (e.g. Lord..., Bishop...) are less well behaved for this purpose.
"""
_honorifics = [
    f"{x} "
    for x in [
        "mr",
        "mrs",
        "miss",
        "ms",
        "dr",
        "sir",
        "rt hon",
    ]
]
_honorifics_regex = re.compile(rf"({'|'.join(_honorifics)})", re.IGNORECASE)


def normalize_name(raw_name: str) -> str:
    """
    Normalize a person's name.

    - Remove honorifics and titles
    - Strip any extraneous whitespace
    - Convert `Surname, Forename` format to `Forename Surname`
    """
    without_honorifics = re.sub(_honorifics_regex, "", raw_name, re.IGNORECASE)

    normalised_whitespace = " ".join(x for x in without_honorifics.split(" ") if x)
    if "," in normalised_whitespace:
        parts = [x.strip() for x in normalised_whitespace.split(",")]
        return f"{' '.join(parts[1:])} {parts[0]}"
    else:
        return normalised_whitespace
