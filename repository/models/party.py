from typing import Optional

from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models import DO_NOTHING

import logging

from repository.models.mixins import (
    WikipediaMixin,
    BaseModel,
    PeriodMixin,
    ParliamentDotUkMixin,
)

log = logging.getLogger(__name__)

# Added to party parliamentdotuk ID in case of multiple parties using same ID
# e.g. Labour shares ID with Labour Co-op
SHARED_ID_OFFSET = 10000


class Party(ParliamentDotUkMixin, WikipediaMixin, BaseModel):
    name = models.CharField(max_length=64, unique=True)
    short_name = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        default=None,
    )
    long_name = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True,
        help_text="Official name",
        default=None,
    )
    homepage = models.URLField(null=True, blank=True)
    year_founded = models.PositiveSmallIntegerField(default=0)

    @property
    def mp_population(self) -> int:
        """Returns number of MPs associated with this party"""
        return self.objects.count()

    def canonical(self) -> "Party":
        try:
            aka = PartyAlsoKnownAs.objects.get(alias=self)
            return aka.canonical
        except (PartyAlsoKnownAs.DoesNotExist, MultipleObjectsReturned):
            return self

    class Meta:
        verbose_name_plural = "Parties"

    def __str__(self):
        return self.name


class PartyAlsoKnownAs(BaseModel):
    canonical = models.ForeignKey(
        "Party",
        on_delete=models.CASCADE,
        help_text="Preferred party instance",
        related_name="canonical",
    )
    alias = models.OneToOneField(
        "Party",
        on_delete=models.CASCADE,
        help_text="An alternative instance, probably with a differently formatted name",
        related_name="alias",
    )

    class Meta:
        verbose_name_plural = "Parties also known as"
        verbose_name = "PartyAlsoKnownAs"

    def __str__(self):
        return f"{self.alias} -> {self.canonical}"


class PartyAssociation(PeriodMixin, BaseModel):
    """Allow tracking of people that have moved between different parties."""

    party = models.ForeignKey(
        "Party",
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="parties",
    )

    def __str__(self):
        return f"{self.person}: {self.party}"

    class Meta:
        unique_together = [
            ["start", "person"],
        ]


class PartyTheme(BaseModel):
    TEXT_COLOR_OPTIONS = [
        ("light", "light"),
        ("dark", "dark"),
    ]

    party = models.OneToOneField(
        Party,
        on_delete=DO_NOTHING,
        null=True,
        blank=True,
        related_name="theme",
    )

    primary_color = models.CharField(max_length=6, help_text="Hex color code")
    accent_color = models.CharField(max_length=6, help_text="Hex color code")
    primary_text_color = models.CharField(
        max_length=5,
        choices=TEXT_COLOR_OPTIONS,
        help_text="Color for text that overlays primary_color",
    )
    accent_text_color = models.CharField(
        max_length=5,
        choices=TEXT_COLOR_OPTIONS,
        help_text="Color for text that overlays accent_color",
    )

    def __str__(self):
        return f"Theme: {self.party}"


def get_or_create_party(
    parliamentdotuk: Optional[int], name: Optional[str]
) -> Optional["Party"]:
    if not parliamentdotuk:
        return None

    max_lookups = 5
    party_id = parliamentdotuk

    for n in range(0, max_lookups):
        party, created = Party.objects.get_or_create(
            parliamentdotuk=party_id,
            defaults={
                "name": name,
            },
        )

        if created:
            # First come, first served
            return party

        elif party.name == name:
            # ID matches the name we have already recorded
            return party

        else:
            party_id = party_id + SHARED_ID_OFFSET

    log.warning(f"Many parties appear to share the same ID: {parliamentdotuk} {name}")
