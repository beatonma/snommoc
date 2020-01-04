"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    PeriodMixin,
)

log = logging.getLogger(__name__)


HOUSE_OF_COMMONS = 'Commons'
HOUSE_OF_LORDS = 'Lords'


class House(BaseModel):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class HouseMembership(PeriodMixin, BaseModel):
    house = models.ForeignKey(
        'House',
        on_delete=models.CASCADE
    )

    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [
            ['start', 'house', 'person'],
        ]
