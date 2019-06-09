from typing import List

from django.db import models

from repository.models import GenericPersonForeignKeyMixin


class PoliticalInterest(GenericPersonForeignKeyMixin, models.Model):
    description = models.CharField(max_length=48)

    @classmethod
    def create(cls, person, interests: List[str]):
        for description in interests:
            PoliticalInterest.objects.create(
                person=person,
                description=description).save()

    def __str__(self):
        return f'{self.description}'


class CountryOfInterest(GenericPersonForeignKeyMixin, models.Model):
    country = models.CharField(max_length=48)

    @classmethod
    def create(cls, person, interests: List[str]):
        for country in interests:
            CountryOfInterest.objects.create(
                person=person,
                country=country).save()

    def __str__(self):
        return f'{self.country}'
