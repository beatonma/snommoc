from common.models import BaseModel
from django.db import models


class ParliamentaryEvent(BaseModel):
    date = models.DateField()

    class Meta:
        ordering = ["-date"]
