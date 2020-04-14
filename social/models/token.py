"""

"""

import logging
import uuid

from django.db import models

from repository.models.mixins import BaseModel

log = logging.getLogger(__name__)


def _create_default_username() -> str:
    return uuid.uuid4().hex[:10]


class SignInServiceProvider(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserToken(BaseModel):
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
    username = models.CharField(max_length=16, default=_create_default_username, unique=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.provider}: {self.token}'
