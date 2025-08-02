from django.db import models

from common.models import BaseModel


class ParliamentaryEvent(BaseModel):
    date = models.DateField()

    class Meta:
        ordering = ["-date"]
