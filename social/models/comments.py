"""

"""

import logging

from django.db import models

from repository.models.mixins import BaseModel
from social.models.mixins import (
    GenericTargetMixin,
    UserMixin,
)

log = logging.getLogger(__name__)


class Comment(UserMixin, GenericTargetMixin, BaseModel):

    text = models.CharField(max_length=240)
    flagged = models.BooleanField(
        default=False,
        help_text='Somebody has flagged this comment for review',
    )
    visible = models.BooleanField(
        default=True,
        help_text='This comment may be displayed publicly',
    )

    class Meta:
        verbose_name_plural = 'Comments'
        verbose_name = 'Comment'

        constraints = [
            models.UniqueConstraint(
                fields=['target_type', 'target_id', 'text', 'user'],
                name='unique_comment_per_user_per_object'
            )
        ]

    def __str__(self):
        return f'{self.target_id} {self.text}'
