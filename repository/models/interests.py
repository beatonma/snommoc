from typing import List

from django.db import models

from repository.models.person import Person

INTEREST_CATEGORY_GENERIC = 'political'
INTEREST_CATEGORY_COUNTRY = 'country'


class Interest(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='interests',
        related_query_name='interest'
    )

    description = models.CharField(max_length=48)
    category = models.CharField(
        max_length=16,
        choices=[
            (INTEREST_CATEGORY_GENERIC, INTEREST_CATEGORY_GENERIC),
            (INTEREST_CATEGORY_COUNTRY, INTEREST_CATEGORY_COUNTRY),
        ],
        default=INTEREST_CATEGORY_GENERIC,
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
                category=INTEREST_CATEGORY_COUNTRY,
            ).save()

    def __str__(self):
        return f'{self.description}'
