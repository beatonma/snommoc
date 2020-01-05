"""

"""

import logging

from django.db import models

from repository.models.mixins import BaseModel

log = logging.getLogger(__name__)


class Town(BaseModel):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(
        'Country',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        unique_together = [
            ['name', 'country'],
        ]


class Country(BaseModel):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = 'Countries'
