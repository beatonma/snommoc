"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    PeriodMixin,
    BaseModel,
    ParliamentDotUkMixin,
)

log = logging.getLogger(__name__)


class ParliamentarySession(ParliamentDotUkMixin, PeriodMixin, BaseModel):
    """A legislative session, usually lasting about a year."""
    name = models.CharField(max_length=24)

    def __str__(self):
        return self.name
