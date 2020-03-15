"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    PersonMixin,
)

log = logging.getLogger(__name__)


class BaseComment(BaseModel):
    text = models.CharField(max_length=240)
    flagged = models.BooleanField(default=False, help_text='Somebody has flagged this commment for review')
    visible = models.BooleanField(default=True, help_text='This comment may be displayed publicly')

    class Meta:
        verbose_name_plural = 'Comments'
        verbose_name = 'Comment'


class PersonComment(BaseComment):
    person = models.ForeignKey(
        'repository.Person',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.person}: {self.text}'


class CommonsDivisionComment(BaseComment):
    division = models.ForeignKey(
        'repository.CommonsDivision',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.division}: {self.text}'


class LordsDivisionComment(BaseComment):
    division = models.ForeignKey(
        'repository.LordsDivision',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.division}: {self.text}'


class BillComment(BaseComment):
    bill = models.ForeignKey(
        'repository.Bill',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.bill}: {self.text}'
