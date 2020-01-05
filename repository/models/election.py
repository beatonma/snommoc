"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
    PersonMixin,
)

log = logging.getLogger(__name__)


class Election(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(
        max_length=32,
        unique=True,
    )
    date = models.DateField()


class ElectionNationalResult(ParliamentDotUkMixin, BaseModel):
    election = models.ForeignKey(
        'Election',
        on_delete=models.CASCADE,
    )

    winning_party = models.ForeignKey(
        'Party',
        on_delete=models.CASCADE,
    )


class ContestedElection(PersonMixin, BaseModel):
    """Elections in which the person took part but did not win."""
    election = models.ForeignKey(
        'Election',
        on_delete=models.CASCADE,
    )

    constituency = models.ForeignKey(
        'Constituency',
        on_delete=models.CASCADE,
    )
