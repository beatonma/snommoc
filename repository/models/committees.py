"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    PeriodMixin,
    ParliamentDotUkMixin,
    PersonMixin,
)

log = logging.getLogger(__name__)


class Committee(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=64, unique=True)


class CommitteeMember(PersonMixin, PeriodMixin, BaseModel):
    committee = models.ForeignKey(
        'Committee',
        on_delete=models.CASCADE,
    )


class CommitteeChair(PeriodMixin, BaseModel):
    member = models.ForeignKey(
        'CommitteeMember',
        on_delete=models.CASCADE,
    )
