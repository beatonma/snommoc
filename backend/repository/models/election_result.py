from django.db import models
from repository.models.mixins import BaseModel
from repository.models.person import NAME_MAX_LENGTH


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
