from typing import List

from django.db import models

from repository.models.people import GenericPersonForeignKeyMixin


INTEREST_CLASSIFICATION_GENERIC = 'political'
INTEREST_CLASSIFICATION_COUNTRY = 'country'


class Interest(GenericPersonForeignKeyMixin, models.Model):
    description = models.CharField(max_length=48)
    classification = models.CharField(
        max_length=16,
        choices=[
            (INTEREST_CLASSIFICATION_GENERIC, INTEREST_CLASSIFICATION_GENERIC),
            (INTEREST_CLASSIFICATION_COUNTRY, INTEREST_CLASSIFICATION_COUNTRY),
        ],
        default='political',
    )

    @classmethod
    def create(cls, person, interests: List[str]):
        for description in interests:
            Interest.objects.create(
                person=person,
                description=description
            ).save()

    @classmethod
    def create_countries(cls, person, countries: List[str]):
        for country in countries:
            Interest.objects.create(
                person=person,
                description=country,
                classification=INTEREST_CLASSIFICATION_COUNTRY,
            ).save()

    def __str__(self):
        return f'{self.description}'
