"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    PersonMixin,
    ParliamentDotUkMixin,
)

log = logging.getLogger(__name__)


class Division(ParliamentDotUkMixin, BaseModel):
    title = models.CharField(max_length=512)
    date = models.DateField()

    session = models.ForeignKey(
        'ParliamentarySession',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    division_number = models.PositiveSmallIntegerField()

    uin = models.CharField(max_length=64)

    ayes = models.PositiveSmallIntegerField(
        help_text='How many members voted for the motion',
    )
    noes = models.PositiveSmallIntegerField(
        help_text='How many members voted against the motion',
    )

    @property
    def passed(self) -> bool:
        """Return True if the Ayes have it, False otherwise."""
        return self.ayes > self.noes

    @property
    def margin(self) -> int:
        return abs(self.ayes - self.noes)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class CommonsDivision(Division):
    deferred_vote = models.BooleanField(
        default=False,
        help_text='A deferred vote is one that is not held immediately '
                  'at the end of the debate, but at a later \'convenient\' time',
    )
    abstentions = models.PositiveSmallIntegerField(
        help_text='How many members abstained from voting',
    )
    did_not_vote = models.PositiveSmallIntegerField()
    errors = models.PositiveSmallIntegerField(
        help_text='How many votes were found to be recorded in error'
    )
    non_eligible = models.PositiveSmallIntegerField(
        help_text='How many members were ineligible to vote in this division',
    )
    suspended_or_expelled = models.PositiveSmallIntegerField(
        help_text='How many members were unable to vote due to suspension or expulsion'
    )


class LordsDivision(Division):
    description = models.CharField(max_length=1024)
    whipped_vote = models.BooleanField(default=False)

    @property
    def contents(self) -> int:
        """Alias for ayes, as used in the House of Lords."""
        return self.ayes

    @property
    def not_contents(self) -> int:
        """Alias for noes, as used in the House of Lords."""
        return self.noes


class DivisionVote(PersonMixin, BaseModel):
    aye = models.BooleanField(default=False)
    no = models.BooleanField(default=False)
    abstention = models.BooleanField(default=False)
    did_not_vote = models.BooleanField(default=False)
    suspended_or_expelled = models.BooleanField(default=False)

    @property
    def vote_type(self):
        if self.aye:
            return 'AyeVote'
        elif self.no:
            return 'NoVote'
        elif self.abstention:
            return 'Abstains'
        elif self.did_not_vote:
            return 'DidNotVote'
        elif self.suspended_or_expelled:
            return 'SuspendedOrExpelledVote'

    class Meta:
        abstract = True


class CommonsDivisionVote(DivisionVote):
    division = models.ForeignKey(
        'CommonsDivision',
        on_delete=models.CASCADE,
        related_name='votes',
    )

    def __str__(self):
        return f'{self.person} [{self.vote_type}]: {self.division}'


class LordsDivisionVote(DivisionVote):
    division = models.ForeignKey(
        'LordsDivision',
        on_delete=models.CASCADE,
        related_name='votes',
    )

    def __str__(self):
        return f'{self.person} [{self.vote_type}]: {self.division}'
