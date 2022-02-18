from django.db import models

from repository.models.mixins import BaseModel


class Organisation(BaseModel):
    """Currently only for BillSponsor but potential for other uses."""

    name = models.CharField(max_length=512)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} [{self.url}]"

    class Meta:
        ordering = ["name"]
