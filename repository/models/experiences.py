"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    PersonMixin,
    PeriodMixin,
)

log = logging.getLogger(__name__)


class ExperienceCategory(BaseModel):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Experience(PersonMixin, PeriodMixin, BaseModel):
    category = models.ForeignKey(
        'ExperienceCategory',
        on_delete=models.CASCADE,
    )

    organisation = models.CharField(max_length=64, null=True, blank=True)
    title = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.category} {self.title}@{self.organisation}'
