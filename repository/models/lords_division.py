from django.db import models
from django.db.models import UniqueConstraint

from repository.models.mixins import BaseModel, ParliamentDotUkMixin


class LordsDivisionRedux(ParliamentDotUkMixin, BaseModel):
    title = models.TextField(null=True, blank=True)
    date = models.DateField()
    number = models.PositiveSmallIntegerField()
    notes = models.TextField(null=True, blank=True)
    is_whipped = models.BooleanField()
    is_government_content = models.BooleanField()
    authoritative_content_count = models.PositiveSmallIntegerField()
    authoritative_not_content_count = models.PositiveSmallIntegerField()
    division_had_tellers = models.BooleanField()
    teller_content_count = models.PositiveSmallIntegerField()
    teller_not_content_count = models.PositiveSmallIntegerField()
    member_content_count = models.PositiveSmallIntegerField()
    member_not_content_count = models.PositiveSmallIntegerField()
    sponsoring_member = models.ForeignKey(
        "repository.Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sponsored_lords_divisions",
    )
    is_house = models.BooleanField(null=True)
    amendment_motion_notes = models.TextField(null=True, blank=True)
    is_government_win = models.BooleanField(null=True, blank=True)
    remote_voting_start = models.DateTimeField(null=True, blank=True)
    remote_voting_end = models.DateTimeField(null=True, blank=True)
    division_was_exclusively_remote = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.date})"


class LordsDivisionMemberVote(BaseModel):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="lords_division_votes",
    )
    division = models.ForeignKey(
        "repository.LordsDivisionRedux",
        on_delete=models.CASCADE,
        related_name="votes",
    )
    vote = models.ForeignKey(
        "repository.DivisionVoteType",
        on_delete=models.CASCADE,
        related_name="+",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["person", "division"],
                name="One vote per Person per LordsDivision",
            ),
        ]

    def __str__(self):
        return f"{self.division.title}: {self.person.name} [{self.vote.name}]"


class DivisionVoteType(BaseModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
