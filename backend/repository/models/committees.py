from common.models import BaseModel
from django.db import models
from repository.models.mixins import ParliamentDotUkMixin, PeriodMixin, PersonMixin
from util.cleanup import Deprecated


class Committee(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.name}"


class CommitteeMember(PersonMixin, PeriodMixin, BaseModel):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="committees",
    )
    committee = models.ForeignKey(
        "Committee",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.person}: {self.committee}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "committee", "start"],
                name="unique_committee_per_person_per_start_date",
            )
        ]


class CommitteeChair(Deprecated, PeriodMixin, BaseModel):
    member = models.ForeignKey(
        "CommitteeMember",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.member}: {self.start} -> {self.end}"
