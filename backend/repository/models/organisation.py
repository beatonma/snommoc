from common.models import BaseModel
from django.db import models


class Organisation(BaseModel):
    name = models.CharField(max_length=512, unique=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} [{self.url}]"

    class Meta:
        ordering = ["name"]
