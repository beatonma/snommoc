from django.db import models

from repository.models.mixins import (
    BaseModel,
    PersonMixin,
    ParliamentDotUkMixin,
)


class InterestCategory(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=64)


class Interest(ParliamentDotUkMixin, PersonMixin, BaseModel):
    category = models.ForeignKey(
        'InterestCategory',
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=160)

    created = models.DateField(blank=True, null=True)
    amended = models.DateField(blank=True, null=True)
    deleted = models.DateField(blank=True, null=True)
    registered_late = models.BooleanField()
