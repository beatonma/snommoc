"""

"""

import logging

from django.db import models

log = logging.getLogger(__name__)


class PeriodMixin(models.Model):
    """For models that represent something with a start/end date"""
    start = models.DateField()
    end = models.DateField(null=True)

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
