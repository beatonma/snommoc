from django.db import models

from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
)
from repository.models.person import NAME_MAX_LENGTH


class ConstituencyResultDetail(ParliamentDotUkMixin, BaseModel):
    """e.g. https://lda.data.parliament.uk/electionresults/382387.json"""

    constituency_result = models.OneToOneField(
        "ConstituencyResult",
        on_delete=models.CASCADE,
        related_name="result_detail",
        null=True,
        blank=True,
    )
    electorate = models.PositiveIntegerField(default=0)
    majority = models.PositiveIntegerField(default=0)
    turnout = models.PositiveIntegerField(default=0)
    turnout_fraction = models.DecimalField(max_digits=3, decimal_places=3)  # 0 < n < 1
    result = models.CharField(max_length=32)

    class Meta:
        ordering = ["constituency_result"]

    def __str__(self):
        return f"{self.constituency_result}"


class ConstituencyCandidate(BaseModel):
    election_result = models.ForeignKey(
        "ConstituencyResultDetail",
        on_delete=models.CASCADE,
        related_name="candidates",
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
    party_name = models.CharField(max_length=128)  # LDA API represents this with TLA

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
        return f"{self.name}: {self.election_result.parliamentdotuk}"
