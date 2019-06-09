from django.db import models


class Constituency(models.Model):
    name = models.CharField(max_length=64)
    mp = models.OneToOneField('Mp', on_delete=models.CASCADE, null=True)
