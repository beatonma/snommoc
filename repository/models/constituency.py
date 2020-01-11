from django.db import models

from repository.models.mixins import (
    PeriodMixin,
    ParliamentDotUkMixin,
    BaseModel,
)


class Constituency(ParliamentDotUkMixin, PeriodMixin, BaseModel):
    name = models.CharField(max_length=64)
    mp = models.OneToOneField(
        'Person',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        help_text='Current representative',
    )

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


class ConstituencyResult(PeriodMixin, BaseModel):
    election = models.ForeignKey(
        'Election',
        on_delete=models.CASCADE,
    )

    mp = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
    )

    constituency = models.ForeignKey(
        'Constituency',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.election}: {self.constituency}'

    class Meta:
        unique_together = [
            ['election', 'constituency'],
            ['election', 'mp'],
        ]


class ConstituencyBoundary(BaseModel):
    constituency = models.OneToOneField(
        Constituency,
        on_delete=models.DO_NOTHING,
    )
    boundary = models.TextField(help_text='KML file content')

    def __str__(self):
        return self.constituency

    class Meta:
        verbose_name_plural = 'Constituency Boundaries'
