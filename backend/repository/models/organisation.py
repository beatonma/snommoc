from django.db import models
from repository.models.mixins import BaseModel


class Organisation(BaseModel):
    name = models.CharField(max_length=512, unique=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} [{self.url}]"

    class Meta:
        ordering = ["name"]
