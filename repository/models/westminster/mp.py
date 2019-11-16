from django.db import models

from repository.models.interests import (
    INTEREST_CATEGORY_COUNTRY,
    INTEREST_CATEGORY_GENERIC,
)
from repository.models.mixins import (
    TheyWorkForYouMixin,
    PeriodMixin,
    ParliamentDotUkMixin,
)
from repository.models.person import Person


class Mp(ParliamentDotUkMixin, TheyWorkForYouMixin, PeriodMixin, models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='mp',
        related_query_name='mp'
    )

    party = models.ForeignKey(
        'Party',
        on_delete=models.DO_NOTHING,
        related_name='mps',
        null=True)

    @property
    def links(self):
        return self.person.links

    @property
    def interests(self):
        return self.person.interests.all()

    @property
    def countries_of_interest(self):
        return self.person.interests.filter(category=INTEREST_CATEGORY_COUNTRY)

    @property
    def generic_interests(self):
        return self.person.interests.filter(category=INTEREST_CATEGORY_GENERIC)

    class Meta:
        verbose_name_plural = 'MPs'
        verbose_name = 'MP'

    def __str__(self):
        return self.person.name
