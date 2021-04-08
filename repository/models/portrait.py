import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
)

log = logging.getLogger(__name__)


class MemberPortrait(BaseModel):
    person = models.OneToOneField(
        'Person',
        on_delete=models.CASCADE
    )

    year_taken = models.PositiveIntegerField(default=0, blank=True, null=True)

    fullsize_url = models.URLField(blank=True, null=True)
    square_url = models.URLField(blank=True, null=True)
    wide_url = models.URLField(blank=True, null=True)
    tall_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Member Portraits'
        verbose_name = 'Member Portrait'

    def __str__(self):
        return f'{self.person}'
