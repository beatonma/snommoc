import logging
import re
from datetime import date as _date
from functools import reduce
from operator import __or__
from typing import List, Optional

from django.db.models import Q

from repository.models import (
    Constituency,
    ConstituencyAlsoKnownAs,
    ConstituencyResult,
    ContestedElection,
    UnlinkedConstituency,
)
from repository.models.mixins import PeriodMixin
from util.time import get_today

log = logging.getLogger(__name__)


def get_constituency_for_date(
    name: str,
    date: Optional[_date],
) -> Optional[Constituency]:
    def _generalised_filter(n: str):
        """Remove punctuation, conjunctions, etc which may not be formatted the
        same way from different sources e.g. 'and' vs '&'."""
        name_regex = (
            re.escape(n)
            .replace(",", ",?")
            .replace("\&", "(&|and)")
            .replace(" and\ ", " (&|and)\ ")
        )

        return {"name__iregex": name_regex}

    if name is None:
        return None

    if date is None:
        date = get_today()

    c = Constituency.objects.filter(**_generalised_filter(name))
    count = c.count()

    # Simple cases
    if count == 0:
        # Name not found - try and resolve the constituency using ConstituencyAlsoKnownAs.
        try:
            return (
                ConstituencyAlsoKnownAs.objects.filter(name=name)
                .filter(PeriodMixin.get_date_in_period_filter(date))
                .first()
                .canonical
            )
        except Exception as e:
            log.info(f"No ConstituencyAKA found for name={name}, date={date}: {e}")
            return None

    elif count == 1:
        # Name found and only one result so no further filtering required
        return c.first()

    # There are multiple results so we have to try filtering by date
    with_valid_date = c.exclude(start=None).order_by("start")

    filtered_by_date = with_valid_date.filter(
        PeriodMixin.get_date_in_period_filter(date)
    )

    if filtered_by_date:
        # Result was found that matches the date requirement
        return filtered_by_date.first()

    earliest = with_valid_date.first()
    if earliest.start > date:
        # Date is before earliest result -> return earliest available result
        return earliest

    # All else fails, return the most recent available result.
    return with_valid_date.last()


def get_current_constituency(name: str) -> Optional[Constituency]:
    return get_constituency_for_date(name, get_today())


def get_suggested_constituencies(name: str, date: _date) -> List[Constituency]:
    """
    Return a list of constituencies that existed at the time of the election
    and have a similar [i.e. matching word(s)] name
    """

    def _remove_substrings(string, chars: list) -> str:
        for c in chars:
            string = string.replace(c, "")

        return string

    def _remove_words(string, words: list) -> str:
        for word in words:
            string = re.sub(rf"\b{word}\b", "", string)

        string = string.replace("  ", " ")

        return string

    stripped_name = _remove_substrings(name, ["&", ","])
    stripped_name = _remove_words(
        stripped_name, ["and", "East", "West", "North", "South"]
    )
    stripped_name = re.sub(
        r"\s+", " ", stripped_name
    )  # Ensure remaining words are separated by only one space
    name_chunks = stripped_name.split(" ")[:5]

    if not name_chunks:
        return []

    name_filters = reduce(__or__, [Q(name__icontains=x) for x in name_chunks])
    date_filter = PeriodMixin.get_date_in_period_filter(date)

    suggestions = Constituency.objects.filter(date_filter).filter(name_filters)

    if not suggestions:
        # If no result using date and name, try again just using name
        suggestions = Constituency.objects.filter(name_filters)

    return suggestions


def resolve_unlinked_constituency(
    unlinked: UnlinkedConstituency, canonical: Constituency
):
    """
    Consume an UnlinkedConstituency instance by linking it with a canonical Constituency.

    Creates an instance of ConstituencyAlsoKnownAs so this can be resolved automatically in the future.

    If person_won, this should be used to create a ConstituencyResult object.
    Otherwise, this should be used to create a ContestedElection object.
    """
    ConstituencyAlsoKnownAs.objects.update_or_create(
        name=unlinked.name,
        canonical=canonical,
        defaults={
            "start": canonical.start,
            "end": canonical.end,
        },
    )

    if unlinked.person_won:
        ConstituencyResult.objects.update_or_create(
            constituency=canonical,
            election=unlinked.election,
            defaults={
                "mp": unlinked.person,
                "start": unlinked.start,
                "end": unlinked.end,
            },
        )

    else:
        ContestedElection.objects.update_or_create(
            person=unlinked.person,
            election=unlinked.election,
            defaults={
                "constituency": canonical,
            },
        )

    unlinked.delete()
