from django.db import models
from django.db.models import UniqueConstraint
from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
    PeriodMixin,
    SocialMixin,
)


class Constituency(SocialMixin, ParliamentDotUkMixin, PeriodMixin, BaseModel):
    name = models.CharField(max_length=64)
    mp = models.OneToOneField(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Current representative",
    )

    ordinance_survey_name = models.CharField(max_length=64, null=True, blank=True)
    gss_code = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        help_text="Government Statistical Service ID",
    )

    def social_title(self) -> str:
        return self.name

    def __str__(self):
        return f"{self.name} [{self.parliamentdotuk}] {self.describe_timespan()}"

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
        null=True,
        blank=True,
        default=None,
    )

    constituency = models.ForeignKey(
        "Constituency",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.election} | {self.constituency}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["election", "constituency", "mp"],
                name="unique_constituency_result",
            )
        ]
        ordering = ["constituency", "election"]


class UnlinkedConstituency(PeriodMixin, BaseModel):
    """
    A placeholder for a constituency which is known by name only.

    [ConstituencyResult] and [ContestedElection] source data only provides a name (no ID),
    and sometimes we are unable to resolve that name to a canonical [Constituency] instance.

    In those cases, create an UnlinkedConstituency which can be checked manually.

    See :py:func:`<repository.resolution.resolve_unlinked_constituency>`
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
    geo_json = models.JSONField()

    def __str__(self):
        return self.constituency.name

    class Meta:
        verbose_name_plural = "Constituency Boundaries"


class ConstituencyAlsoKnownAs(PeriodMixin, BaseModel):
    canonical = models.ForeignKey(
        "Constituency",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )
    name = models.CharField(max_length=64, default="")

    def __str__(self):
        return f"{self.name} -> {self.canonical.name} [{self.canonical_id}]"

    class Meta:
        verbose_name_plural = "Constituency AKAs"
