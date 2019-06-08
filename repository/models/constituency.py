from django.db import models

from repository.models import Mp


class Constituency(models.Model):
    name = models.CharField(max_length=64)
    mp = models.OneToOneField(Mp, on_delete=models.CASCADE)
