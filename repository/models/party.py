from django.db import models


class Party(models.Model):
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=16)
    long_name = models.CharField(max_length=64)
