import re
from typing import Optional

from django.db.models import Q, QuerySet

from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS
from repository.models import Constituency, Election, Person, Party

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


def get_active_members(**kwargs) -> QuerySet[Person]:
    return Person.objects.filter(active=True, **kwargs)


def get_active_mps(**kwargs) -> QuerySet[Person]:
    return get_active_members(house__name=HOUSE_OF_COMMONS, **kwargs)


def get_active_lords(**kwargs) -> QuerySet[Person]:
    return get_active_members(house__name=HOUSE_OF_LORDS, **kwargs)


def get_active_party_members(party: Party, **kwargs) -> QuerySet[Person]:
    return get_active_members(party=party, **kwargs)


def get_party_mps(party: Party, **kwargs) -> QuerySet[Person]:
    return get_active_party_members(party=party, house__name=HOUSE_OF_COMMONS, **kwargs)


def get_party_lords(party: Party, **kwargs) -> QuerySet[Person]:
    return get_active_party_members(party=party, house__name=HOUSE_OF_LORDS, **kwargs)


def normalize_name(raw_name: str) -> str:
    """
    Normalize a person's name.

    - Remove honorifics and titles
    - Strip any extraneous whitespace
    - Convert `Surname, Forename` format to `Forename Surname`
    """
    without_honorifics = re.sub(_honorifics_regex, "", raw_name, re.IGNORECASE)

    normalised_whitespace = " ".join([x for x in without_honorifics.split(" ") if x])
    if "," in normalised_whitespace:
        parts = [x.strip() for x in normalised_whitespace.split(",")]
        return f"{' '.join(parts[1:])} {parts[0]}"
    else:
        return normalised_whitespace


def get_member_by_name(name: str) -> Optional[Person]:
    """
    Try to resolve the given name to a Person instance.

    If the name came from a 3rd party API, consider passing it through normalize_name first.
    """
    by_name = Person.objects.filter(
        Q(name__iexact=name) | Q(personalsoknownas__alias__iexact=name),
    )

    if by_name.count() == 1:
        return by_name.first()


def get_member_for_election_result(
    name: str,
    constituency: Constituency,
    election: Election,
) -> Optional[Person]:
    by_name = Person.objects.filter(
        Q(name__iexact=name) | Q(personalsoknownas__alias__iexact=name),
    )

    if by_name.count() == 1:
        return by_name.first()

    by_constituency = by_name.filter(
        Q(constituency=constituency)
        | (
            Q(contestedelection__constituency=constituency)
            & Q(contestedelection__election=election)
        )
    )

    if by_constituency.count() == 1:
        return by_constituency.first()
