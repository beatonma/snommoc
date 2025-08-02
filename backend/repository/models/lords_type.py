from django.db import models

from common.models import BaseModel


class LordsType(BaseModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
