from django.db import models
from django.db.models import UniqueConstraint

from repository.models.houses import HOUSE_OF_LORDS
from repository.models.mixins import BaseModel, ParliamentDotUkMixin


class LordsDivision(ParliamentDotUkMixin, BaseModel):
    title = models.TextField(null=True, blank=True)
    date = models.DateField()
    number = models.PositiveSmallIntegerField()
    amendment_motion_notes = models.TextField(null=True, blank=True)
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
    is_government_win = models.BooleanField(null=True, blank=True)
    remote_voting_start = models.DateTimeField(null=True, blank=True)
    remote_voting_end = models.DateTimeField(null=True, blank=True)
    division_was_exclusively_remote = models.BooleanField(null=True, blank=True)

    @property
    def house(self) -> str:
        return HOUSE_OF_LORDS

    @property
    def passed(self) -> bool:
        return self.ayes > self.noes

    @property
    def ayes(self) -> int:
        return self.authoritative_content_count

    @property
    def noes(self) -> int:
        return self.authoritative_not_content_count

    def __str__(self):
        return f"{self.title} ({self.date})"


class LordsDivisionVote(BaseModel):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="lords_division_votes",
    )
    division = models.ForeignKey(
        "repository.LordsDivision",
        on_delete=models.CASCADE,
        related_name="votes_redux",
    )
    vote_type = models.ForeignKey(
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
        ordering = [
            "-modified_on",
        ]

    def __str__(self):
        return f"{self.division.title}: {self.person.name} [{self.vote_type.name}]"


class DivisionVoteType(BaseModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
