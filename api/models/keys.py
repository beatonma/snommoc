import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import (
    User,
    Permission,
)

from api.models.permissions import READ_SNOMMOC_API


class ApiKey(models.Model):
    class Meta:
        permissions = (
            (READ_SNOMMOC_API, 'Can read data from the snommoc API.'),
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.user}'


def grant_read_snommoc_api(user: User):
    content_type = ContentType.objects.get_for_model(ApiKey)
    read_permission = Permission.objects.get(
        codename=READ_SNOMMOC_API,
        content_type=content_type,
    )
    user.user_permissions.add(read_permission)
    user.save()
