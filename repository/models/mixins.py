"""

"""

import logging

from django.db import models

log = logging.getLogger(__name__)


class PeriodMixin(models.Model):
    """For models that represent something with a start/end date"""
    start = models.DateField(null=True)
    end = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


class ParliamentDotUkMixin(models.Model):
    """For models that have a corresponding api on parliament.uk"""
    parliamentdotuk = models.PositiveIntegerField(
        unique=True,
        null=True,
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
        max_length=64,
        help_text='Path section of a wikipedia url (e.g. \'John_Baron_(politician)\')')

    class Meta:
        abstract = True
