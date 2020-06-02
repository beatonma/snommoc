"""

"""

import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from repository.models.mixins import BaseModel

log = logging.getLogger(__name__)


class Comment(BaseModel):
    user = models.ForeignKey(
        'UserToken',
        on_delete=models.DO_NOTHING,
    )

    target_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_type', 'target_id')

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

    def __str__(self):
        return f'{self.target_id} {self.text}'
