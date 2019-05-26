import uuid
from django.db import models
from django.contrib.auth.models import User


class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.user}'
