"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    PeriodMixin,
)

log = logging.getLogger(__name__)


class BaseFeatured(PeriodMixin, BaseModel):
    """Use start/end to define a period during which the item is featured.
    """

    class Meta:
        abstract = True


class FeaturedPerson(BaseFeatured):
    person = models.ForeignKey(
        'repository.Person',
        on_delete=models.CASCADE,
        related_name='+',
    )

    def __str__(self):
        return f'{self.person}: {self.start} -> {self.end}'


class FeaturedBill(BaseFeatured):
    bill = models.ForeignKey(
        'repository.Bill',
        on_delete=models.CASCADE,
        related_name='+',
    )

    def __str__(self):
        return f'{self.bill}: {self.start} -> {self.end}'
