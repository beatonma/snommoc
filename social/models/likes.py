"""

"""

import logging

from django.db import models

from repository.models.mixins import BaseModel

log = logging.getLogger(__name__)


class BaseLike(BaseModel):
    pass


class PersonLike(BaseLike):
    person = models.ForeignKey(
        'repository.Person',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Like: {self.person}'


class CommonsDivisionLike(BaseLike):
    division = models.ForeignKey(
        'repository.CommonsDivision',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Like: {self.division}'


class LordsDivisionLike(BaseLike):
    division = models.ForeignKey(
        'repository.LordsDivision',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Like: {self.division}'


class BillLike(BaseLike):
    bill = models.ForeignKey(
        'repository.Bill',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Like: {self.bill}'
