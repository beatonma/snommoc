import uuid

from django.conf import settings
from django.db import models

from api.permissions import READ_SNOMMOC_API


class ApiKey(models.Model):
    class Meta:
        permissions = ((READ_SNOMMOC_API, "Can read data from the snommoc API."),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.user}"
