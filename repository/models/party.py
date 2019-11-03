from django.db import models

from repository.models.mixins import WikipediaMixin


class Party(WikipediaMixin, models.Model):
    name = models.CharField(max_length=32, unique=True)
    short_name = models.CharField(max_length=16, unique=True)
    long_name = models.CharField(
        max_length=64,
        unique=True,
        help_text='Official name',
    )
    homepage = models.URLField(null=True, blank=True)
    year_founded = models.PositiveSmallIntegerField(default=0)

    @classmethod
    def create(cls, name, short_name, long_name) -> 'Party':
        party = cls(name=name, short_name=short_name, long_name=long_name)
        party.save()
        return party

    class Meta:
        verbose_name_plural = 'Parties'

    def __str__(self):
        return self.name
