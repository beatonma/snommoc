import logging

from django.db import models

UNKNOWN_ID = 0
NAME_MAX_LENGTH = 72

log = logging.getLogger(__name__)


class Person(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text='Canonical name for this person.')

    given_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text='First name',
        null=True)

    family_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text='Last name',
        null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'People'
