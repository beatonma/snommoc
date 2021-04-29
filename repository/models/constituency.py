import datetime
import re
from typing import Optional

from django.db import models
from django.db.models import Q, UniqueConstraint

from repository.models.mixins import (
    PeriodMixin,
    ParliamentDotUkMixin,
    BaseModel,
)


class Constituency(ParliamentDotUkMixin, PeriodMixin, BaseModel):
    name = models.CharField(max_length=64)
    mp = models.OneToOneField(
        "Person",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        help_text="Current representative",
    )

    ordinance_survey_name = models.CharField(max_length=64, null=True, blank=True)
    gss_code = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        help_text="Government Statistical Service ID",
    )
    constituency_type = models.CharField(
        max_length=10,
        null=True,
        choices=[
            ("county", "County"),
            ("borough", "Borough"),
        ],
        help_text="Borough, county...",
    )

    @property
    def is_extant(self) -> bool:
        """Return True if this constituency still exists.
        i.e. It has not undergone boundary/name changes and is represented by
        an MP in parliament."""
        return self.end is None

    @property
    def canonical(self) -> "Constituency":
        try:
            return ConstituencyAlsoKnownAs.objects.get(alias=self).canonical
        except:
            return self

    def __str__(self):
        return f"{self.name} {self.parliamentdotuk} {self.start} - {self.end} {self.gss_code} {self.mp}"

    class Meta:
        verbose_name_plural = "Constituencies"


class ConstituencyResult(PeriodMixin, BaseModel):
    """
    Track which MP won in this constituency at this election.
    """

    election = models.ForeignKey(
        "Election",
        on_delete=models.CASCADE,
    )

    mp = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )

    constituency = models.ForeignKey(
        "Constituency",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.election}: {self.constituency}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["election", "constituency", "mp"],
                name="unique_constituency_result",
            )
        ]


class UnlinkedConstituency(PeriodMixin, BaseModel):
    """
    A placeholder for a constituency which is known by name only.

    [ConstituencyResult] and [ContestedElection] source data only provides a name (no ID),
    and sometimes we are unable to resolve that name to a canonical [Constituency] instance.

    In those cases, create an UnlinkedConstituency which can be checked manually.

    TODO
        Once resolved:
        - If person_won, and start/end values are set, this should be used to create a ConstituencyResult object.
        - Otherwise, this should be used to create a ContestedElection object.
    """

    name = models.CharField(max_length=64)
    election = models.ForeignKey(
        "Election",
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )

    person_won = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Unlinked constituencies"
        constraints = [
            UniqueConstraint(
                fields=["name", "person", "election"],
                name="unique_election_result",
            )
        ]


class ConstituencyBoundary(BaseModel):
    constituency = models.OneToOneField(
        Constituency,
        on_delete=models.CASCADE,
    )
    boundary_kml = models.TextField(help_text="KML file content")
    center_latitude = models.CharField(max_length=24)
    center_longitude = models.CharField(max_length=24)
    area = models.CharField(max_length=24)
    boundary_length = models.CharField(max_length=24)

    def __str__(self):
        return self.constituency.name

    class Meta:
        verbose_name_plural = "Constituency Boundaries"


class ConstituencyAlsoKnownAs(BaseModel):
    canonical = models.ForeignKey(
        "Constituency",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )
    alias = models.OneToOneField(
        "Constituency",
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.alias.name} [{self.alias_id}] -> {self.canonical.name} [{self.canonical_id}]"

    class Meta:
        verbose_name_plural = "Constituency AKAs"


def get_constituency_for_date(
    name: str, date: Optional[datetime.date]
) -> Optional[Constituency]:
    def _generalised_filter(n: str):
        """Remove punctuation, conjunctions, etc which may not be formatted the
        same way from different sources e.g. 'and' vs '&'."""
        name_regex = (
            re.escape(n)
            .replace(",", ",?")
            .replace("&", "(&|and)")
            .replace(" and ", " (&|and) ")
        )

        return {"name__iregex": name_regex}

    c = Constituency.objects.filter(**_generalised_filter(name))
    count = c.count()

    # Simple cases
    if count == 0:
        return None

    elif count == 1:
        return c.first()

    if date is None:
        date = datetime.date.today()

    # More complicated
    with_start = c.exclude(start=None).order_by("start")

    filtered_by_date = with_start.filter(
        Q(start__lte=date) & (Q(end__gt=date) | Q(end__isnull=True))
    )

    if filtered_by_date:
        # Result was found that matches the date requirement
        return filtered_by_date.first()

    if with_start.count() == 0:
        # No useful date, just return the first result.
        return c.first()

    earliest = with_start.first()
    if earliest.start > date:
        # Date is before earliest result -> return earliest available result
        return earliest

    # All else fails, return the latest available result.
    return with_start.last()


def get_current_constituency(name: str) -> Optional[Constituency]:
    return get_constituency_for_date(name, datetime.date.today())
