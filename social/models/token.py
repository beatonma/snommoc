"""

"""

import logging
import uuid

from django.core.validators import RegexValidator
from django.db import models

from repository.models.mixins import BaseModel
from social.models.mixins import DeletionPendingMixin

log = logging.getLogger(__name__)


def _create_default_username() -> str:
    return uuid.uuid4().hex[:10]


class SignInServiceProvider(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserToken(DeletionPendingMixin, BaseModel):
    provider = models.ForeignKey(
        'SignInServiceProvider',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    provider_account_id = models.CharField(
        max_length=100,
        unique=True,
        editable=False,
    )
    token = models.UUIDField(default=uuid.uuid4)
    username = models.CharField(
        max_length=16,
        default=_create_default_username,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9a-zA-Z][0-9a-zA-Z-_.]{2,}[0-9a-zA-Z]$',
                message='Must start and end with alphanumerics. '
                        'Otherwise also allow dash, underscore, dot. '
                        'Minimum 4 characters.',
            )
        ]
    )
    enabled = models.BooleanField(default=True)

    def mark_pending_deletion(self):
        super().mark_pending_deletion()
        self.enabled = False

    def __str__(self):
        return f'{self.provider}: {self.token}'


class UsernameChanged(BaseModel):
    """Created when a UserToken username is changed"""
    token = models.ForeignKey(
        'UserToken',
        on_delete=models.CASCADE,
    )
    new_name = models.CharField(max_length=16)
    previous_name = models.CharField(max_length=16)
