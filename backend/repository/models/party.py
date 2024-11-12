import logging
from typing import Optional

from django.db import models
from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
    PeriodMixin,
    WikipediaMixin,
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

    class Meta:
        verbose_name_plural = "Parties"
        ordering = ["name"]

    def __str__(self):
        return self.name


class PartyAlsoKnownAs(BaseModel):
    canonical = models.ForeignKey(
        "Party",
        on_delete=models.CASCADE,
        help_text="Preferred party instance",
        related_name="aliases",
        null=True,
        blank=True,
    )
    alias = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = "Parties also known as"
        verbose_name = "PartyAlsoKnownAs"
        ordering = ["canonical__name", "alias"]

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
        ("#ffffff", "light"),
        ("#000000", "dark"),
    ]

    party = models.OneToOneField(
        Party,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="theme",
    )

    primary = models.CharField(max_length=10, help_text="Hex color code")
    on_primary = models.CharField(
        max_length=10,
        choices=TEXT_COLOR_OPTIONS,
        help_text="Color for text that overlays primary",
    )

    accent = models.CharField(max_length=10, help_text="Hex color code")
    on_accent = models.CharField(
        max_length=10,
        choices=TEXT_COLOR_OPTIONS,
        help_text="Color for text that overlays accent",
    )

    def __str__(self):
        return f"Theme: {self.party}"


def get_or_create_party(
    parliamentdotuk: Optional[int],
    name: Optional[str],
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
