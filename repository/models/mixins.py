"""

"""
import datetime
import logging

from django.db import models

from util.time import (
    is_current,
    in_range,
)

log = logging.getLogger(__name__)


class BaseModel(models.Model):
    """
    Not a mixin as such. All concrete model implementations should extend from this.
    """
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PersonMixin(models.Model):
    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class PeriodMixin(models.Model):
    """For models that represent something with a start/end date"""
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    @property
    def is_current(self) -> bool:
        return is_current(self.start, self.end)

    def contains(self, other_date: datetime.date) -> bool:
        return in_range(other_date, self.start, self.end)

    class Meta:
        abstract = True


class ParliamentDotUkMixin(models.Model):
    """For models that have a corresponding api on parliament.uk"""
    parliamentdotuk = models.PositiveIntegerField(
        primary_key=True,
        unique=True,
        help_text='ID used on parliament.uk website')

    class Meta:
        abstract = True


class TheyWorkForYouMixin(models.Model):
    """For models that have a corresponding api on theyworkforyou.com"""
    theyworkforyou = models.PositiveIntegerField(
        unique=True,
        null=True,
        help_text='ID used on theyworkforyou.com')

    class Meta:
        abstract = True


class WikipediaMixin(models.Model):
    wikipedia = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text='Path section of a wikipedia url (e.g. \'John_Baron_(politician)\')')

    class Meta:
        abstract = True
