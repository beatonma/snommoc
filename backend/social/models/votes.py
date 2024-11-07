"""
Allow users to register how they would vote on a given division,
or whether they are in favour of or against a bill.
"""

from django.db import models
from repository.models.mixins import BaseModel
from social.models.mixins import GenericTargetMixin, UserMixin


class Vote(UserMixin, GenericTargetMixin, BaseModel):
    class VoteTypeChoices(models.TextChoices):
        AYE = "aye"
        NO = "no"

    vote_type = models.CharField(max_length=10, choices=VoteTypeChoices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["target_type", "target_id", "user"],
                name="unique_user_vote_per_target",
            )
        ]

    def __str__(self):
        return f"{self.user}: {self.vote_type}"
