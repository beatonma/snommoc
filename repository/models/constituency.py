from django.db import models

from repository.models.mixins import (
    PeriodMixin,
    ParliamentDotUkMixin,
)


class Constituency(ParliamentDotUkMixin, PeriodMixin, models.Model):
    name = models.CharField(max_length=64)
    mp = models.OneToOneField(
        'Mp',
        on_delete=models.SET_NULL,
        related_name='constituency',
        null=True)

    ordinance_survey_name = models.CharField(max_length=64, null=True, blank=True)
    gss_code = models.CharField(
        max_length=12, null=True, blank=True,
        help_text='Government Statistical Service ID')
    constituency_type = models.CharField(
        max_length=10, null=True,
        choices=[
            ('county', 'County'),
            ('borough', 'Borough'),
        ],
        help_text='Borough, county...')

    @property
    def is_extant(self) -> bool:
        """Return True if this constituency still exists.
        i.e. It has not undergone boundary/name changes and is represented by
        an MP in parliament."""
        return self.end is None

    def __str__(self):
        return f'{self.name}: {self.mp if self.mp else "No MP"}'

    class Meta:
        verbose_name_plural = 'Constituencies'


class ConstituencyBoundary(models.Model):
    constituency = models.OneToOneField(Constituency, on_delete=models.CASCADE)
    boundary = models.TextField(help_text='KML file content')
