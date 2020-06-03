"""
Allow users to register how they would vote on a given division,
or whether they are in favour of or against a bill.
Maybe use as like/dislike for member favourability too?
"""

import logging

from django.db import models

from repository.models.mixins import BaseModel
from social.models.mixins import (
    GenericTargetMixin,
    UserMixin,
)

log = logging.getLogger(__name__)


class Vote(UserMixin, GenericTargetMixin, BaseModel):
    vote_type = models.ForeignKey(
        'VoteType',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['target_type', 'target_id', 'user'],
                name='unique_user_vote_per_target'
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.vote_type}'


class VoteType(BaseModel):
    name = models.CharField(unique=True, max_length=16)

    def __str__(self):
        return f'{self.name}'
