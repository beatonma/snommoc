"""

"""

import logging
import uuid

from django.db import models

from repository.models.mixins import BaseModel

log = logging.getLogger(__name__)


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
    )
    token = models.UUIDField(default=uuid.uuid4)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.provider}: {self.token}'
