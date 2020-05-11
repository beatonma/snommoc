"""

"""

import logging

from django.db import models

from repository.models.mixins import BaseModel

log = logging.getLogger(__name__)


class UpdateError(BaseModel):
    parliamentdotuk = models.PositiveIntegerField()
    error_message = models.CharField(max_length=1024)
    handled = models.BooleanField(default=False)

    @classmethod
    def create(cls, parliamentdotuk, error):
        cls.objects.create(
            parliamentdotuk=parliamentdotuk,
            error_message=str(error),
        ).save()

    class Meta:
        abstract = True


class BillUpdateError(UpdateError):

    class Meta:
        verbose_name_plural = 'BillUpdateErrors'
        verbose_name = 'BillUpdateError'

    def __str__(self):
        return f'Bill {self.parliamentdotuk}'


class CommonsDivisionUpdateError(UpdateError):

    class Meta:
        verbose_name_plural = 'CommonsDivisionUpdateErrors'
        verbose_name = 'CommonsDivisionUpdateError'

    def __str__(self):
        return f'Commons Division {self.parliamentdotuk}'


class LordsDivisionUpdateError(UpdateError):
    class Meta:
        verbose_name_plural = 'LordsDivisionUpdateErrors'
        verbose_name = 'LordsDivisionUpdateError'

    def __str__(self):
        return f'Lords Division {self.parliamentdotuk}'


class ElectionResultUpdateError(UpdateError):
    class Meta:
        verbose_name_plural = "ElectionResult Update Errors"
        verbose_name = "ElectionResult Update Error"

    def __str__(self):
        return f'{self.parliamentdotuk}'
