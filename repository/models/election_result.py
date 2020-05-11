"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
)
from repository.models.person import NAME_MAX_LENGTH

log = logging.getLogger(__name__)


class ElectionResult(ParliamentDotUkMixin, BaseModel):
    """e.g. https://lda.data.parliament.uk/electionresults/382387.json"""
    constituency = models.ForeignKey(
        'Constituency',
        on_delete=models.CASCADE,
    )
    election = models.ForeignKey(
        'Election',
        on_delete=models.CASCADE,
    )
    electorate = models.PositiveIntegerField(default=0)
    majority = models.PositiveIntegerField(default=0)
    turnout = models.PositiveIntegerField(default=0)
    turnout_fraction = models.DecimalField(max_digits=3, decimal_places=3) # 0 < n < 1
    result = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.constituency}'


class ConstituencyCandidate(BaseModel):
    election_result = models.ForeignKey(
        'ElectionResult',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    votes = models.PositiveSmallIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=100)
    party = models.CharField(max_length=16)  # LDA API represents this with TLA

    class Meta:
        unique_together = [
            ['election_result', 'name'],
        ]

    def __str__(self):
        return f'{self.name}'
