from django.db import models
from django.db.models import DO_NOTHING

from repository.models.mixins import WikipediaMixin


class Party(WikipediaMixin, models.Model):
    name = models.CharField(max_length=32, unique=True)
    short_name = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        default=None,
    )
    long_name = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        help_text='Official name',
        default=None,
    )
    homepage = models.URLField(null=True, blank=True)
    year_founded = models.PositiveSmallIntegerField(default=0)

    @property
    def mp_population(self) -> int:
        """Returns number of MPs associated with this party"""
        return self.objects.count()

    @classmethod
    def create(cls, name, short_name, long_name) -> 'Party':
        party = cls(name=name, short_name=short_name, long_name=long_name)
        party.save()
        return party

    class Meta:
        verbose_name_plural = 'Parties'

    def __str__(self):
        return self.name


class PartyTheme(models.Model):
    TEXT_COLOR_OPTIONS = [
        ('light', 'light'),
        ('dark', 'dark'),
    ]

    party = models.OneToOneField(
        Party,
        on_delete=DO_NOTHING,
        null=True,
        blank=True,
        related_name='theme',
    )

    primary_color = models.CharField(max_length=6, help_text='Hex color code')
    accent_color = models.CharField(max_length=6, help_text='Hex color code')
    primary_text_color = models.CharField(
        max_length=5,
        choices=TEXT_COLOR_OPTIONS,
        help_text='Color for text that overlays primary_color',
    )
    accent_text_color = models.CharField(
        max_length=5,
        choices=TEXT_COLOR_OPTIONS,
        help_text='Color for text that overlays accent_color',
    )
