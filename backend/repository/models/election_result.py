from common.models import BaseModel
from django.db import models
from repository.models.mixins import PeriodMixin, PeriodQuerySet, UnresolvedQuerySet
from repository.models.person import NAME_MAX_LENGTH


class ConstituencyResultQuerySet(UnresolvedQuerySet, PeriodQuerySet):
    def unresolved(self):
        return self.filter(mp__isnull=True)


class ConstituencyResult(PeriodMixin, BaseModel):
    """
    Track which MP won in this constituency at this election.
    """

    objects = ConstituencyResultQuerySet.as_manager()
    election = models.ForeignKey(
        "Election",
        on_delete=models.CASCADE,
    )
    constituency = models.ForeignKey(
        "Constituency",
        on_delete=models.CASCADE,
    )

    winner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="constituency_results",
        related_query_name="constituency_result",
    )
    winner_name = models.CharField(max_length=NAME_MAX_LENGTH, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.winner:
            # If mp has been resolved, mp_name is no longer needed.
            self.winner_name = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.election} | {self.constituency}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["election", "constituency"],
                name="unique_constituency_result",
            )
        ]
        ordering = ["constituency", "election"]


class ConstituencyResultDetail(BaseModel):
    constituency_result = models.OneToOneField(
        "ConstituencyResult",
        on_delete=models.CASCADE,
        related_name="detail",
    )
    result = models.CharField(max_length=32)
    majority = models.PositiveIntegerField(default=0)
    turnout = models.PositiveIntegerField(default=0)
    electorate = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["constituency_result"]

    def __str__(self):
        return f"{self.constituency_result}"


class ConstituencyCandidate(BaseModel):
    election_result = models.ForeignKey(
        "ConstituencyResultDetail",
        on_delete=models.CASCADE,
        related_name="candidates",
        related_query_name="candidate",
    )
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    votes = models.PositiveIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=100)
    party_name = models.CharField(max_length=128)

    party = models.ForeignKey(
        "Party",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        unique_together = [
            ["election_result", "name"],
        ]
        ordering = ["name", "election_result"]

    def __str__(self):
        return f"{self.name}: {self.election_result}"
