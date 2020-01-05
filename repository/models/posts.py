"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
    PeriodMixin,
    PersonMixin,
)

log = logging.getLogger(__name__)


class BasePost(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=96, unique=True)
    hansard_name = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class GovernmentPost(BasePost):
    pass


class ParliamentaryPost(BasePost):
    pass


class OppositionPost(BasePost):
    pass


class BasePostMember(PersonMixin, PeriodMixin, BaseModel):
    class Meta:
        abstract = True


class GovernmentPostMember(BasePostMember):
    post = models.ForeignKey(
        'GovernmentPost',
        on_delete=models.CASCADE,
    )


class ParliamentaryPostMember(BasePostMember):
    post = models.ForeignKey(
        'ParliamentaryPost',
        on_delete=models.CASCADE,
    )


class OppositionPostMember(BasePostMember):
    post = models.ForeignKey(
        'OppositionPost',
        on_delete=models.CASCADE,
    )
