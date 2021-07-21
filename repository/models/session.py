from django.db import models

from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
    PeriodMixin,
)


class ParliamentarySession(ParliamentDotUkMixin, PeriodMixin, BaseModel):
    """A legislative session, usually lasting about a year."""

    name = models.CharField(max_length=24)

    def __str__(self):
        return self.name
