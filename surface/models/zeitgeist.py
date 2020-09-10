"""

"""

import logging

from django.db import models

from repository.models.mixins import BaseModel
from social.models.mixins import GenericTargetMixin

log = logging.getLogger(__name__)


class ZeitgeistItem(GenericTargetMixin, BaseModel):
    REASON_FEATURE = 'feature'
    REASON_SOCIAL = 'social'

    """
    Represents something that is important now, because of social interaction
    or they have been featured..
    """
    reason = models.CharField(
        max_length=24,
        choices=[
            (REASON_FEATURE, REASON_FEATURE),
            (REASON_SOCIAL, REASON_SOCIAL),
        ],
    )

    class Meta:
        verbose_name_plural = 'Zeitgeist items'
        verbose_name = 'Zeitgeist item'
        unique_together = [
            ['target_id', 'target_type'],
        ]

    def __str__(self):
        return f'{self.target} [{self.reason}]'
