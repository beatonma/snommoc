import re
from typing import Self, Union, cast

from common.models import BaseModel, BaseQuerySet
from django.db import models
from django.db.models import Q
from repository.models.mixins import (
    AsciiNameMixin,
    ParliamentDotUkMixin,
    PeriodMixin,
    WikipediaMixin,
)

_SUB_PARTY_ID_OFFSET = 100_000

# Special case:
# Labour and Labour Co-op share the same parliamentdotuk ID but are generally
# distinct, though overlapping, entities.
# https://en.wikipedia.org/wiki/Labour_and_Co-operative_Party
#
# We will track them separately via custom a ID for Labour Co-op.
# QuerySet methods must recognise this and handle it transparently.
_LABOUR_ID = 15  # parliamentdotuk ID for Labour party
_LABOUR_COOP_ID = _LABOUR_ID + _SUB_PARTY_ID_OFFSET  # Synthetic ID


class PartyQuerySet(BaseQuerySet):
    @staticmethod
    def reverse_party_id(party_id: int) -> Q:
        q = Q(party__parliamentdotuk=party_id)
        if party_id == _LABOUR_ID:
            q |= Q(party__parliamentdotuk=_LABOUR_COOP_ID)

        return q

    def update_or_create(
        self,
        defaults=None,
        _resolve_internal: bool = False,
        **kwargs,
    ):
        """Disabled: use `PartyQuerySet.resolve()` instead"""
        if _resolve_internal:
            # Only allow use if called internally by resolve method.
            # _resolve_internal is passed on so that it is received by get_or_create
            # when called in super() implementation.
            return super().update_or_create(
                defaults=defaults, _resolve_internal=_resolve_internal, **kwargs
            )

        raise NotImplementedError(
            f"Use Party.objects.resolve instead of update_or_create ({self} default={defaults}, kwargs={kwargs})"
        )

    def get_or_create(self, defaults=None, _resolve_internal: bool = False, **kwargs):
        """Disabled: use `PartyQuerySet.resolve()` instead"""
        if _resolve_internal:
            # Only allow use if called internally by resolve method.
            # _resolve_internal is stripped here so it is not used in model
            # creation or filtering.
            return super().get_or_create(defaults=defaults, **kwargs)

        raise NotImplementedError(
            f"Use Party.objects.resolve instead of get_or_create ({self} default={defaults}, kwargs={kwargs})"
        )

    def filter(self, *args, **kwargs) -> Self:
        return cast("PartyQuerySet", super().filter(*args, **kwargs))

    def search(self, query: str) -> Self:
        query = query.strip()
        return self.filter(
            Q(name__icontains=query)
            | Q(short_name__icontains=query)
            | Q(long_name__icontains=query)
            | Q(ascii_name__icontains=query)
        )

    def resolve(
        self,
        parliamentdotuk: int | None = None,
        name: str | None = None,
        defaults: dict | None = None,
        update: bool = False,
    ) -> tuple[Union["Party", None], bool]:
        """
        Args:
            parliamentdotuk: Party ID, if available.
            name: Party name, if available.
            defaults: Default values passed to create/update methods, if possible.
            update: If True, update_or_create may be used internally.
                    If False, get_or_create may be used internally.

        Returns:
            A tuple of the (resolved party, created).
            Similar to get_or_create, except that the resolved party may be None!
        """

        defaults = {**(defaults or {})}
        if re.match(r"Labour \(?Co-?op\)?", name or "", re.IGNORECASE):
            # Special case: Labour and Labour Co-op share the same parliamentdotuk
            # ID but are generally consider to be distinct.
            parliamentdotuk = _LABOUR_COOP_ID

        if parliamentdotuk and name:
            defaults["name"] = name

            func = self.update_or_create if update else self.get_or_create
            return func(
                parliamentdotuk=parliamentdotuk,
                defaults=defaults,
                _resolve_internal=True,
            )

        if parliamentdotuk:
            return self.get_or_none(parliamentdotuk=parliamentdotuk), False

        if name:
            return self.get_or_none(name__iexact=name), False

        return None, False

    def current(self):
        return self.filter(territory__isnull=False)


class Party(
    ParliamentDotUkMixin,
    WikipediaMixin,
    AsciiNameMixin,
    BaseModel,
):
    objects = PartyQuerySet.as_manager()
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
    logo = models.FileField(upload_to="party_logo", null=True, blank=True)
    logo_mask = models.FileField(upload_to="party_logo_mask", null=True, blank=True)

    active_member_count = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.update_ascii_name(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Parties"
        ordering = ["name"]


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


class PartyAffiliation(PeriodMixin, BaseModel):
    """Allow tracking of people that have moved between different parties."""

    party = models.ForeignKey(
        "Party",
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="party_affiliations",
    )

    def __str__(self):
        return f"{self.person}: {self.party}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["start", "person", "party"],
                name="unique_party_per_person_per_startdate",
            )
        ]
        ordering = PeriodMixin.meta_ordering_recent()


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

    accent = models.CharField(
        max_length=10, help_text="Hex color code", default="#ffffff"
    )
    on_accent = models.CharField(
        max_length=10,
        choices=TEXT_COLOR_OPTIONS,
        default="#000000",
        help_text="Color for text that overlays accent",
    )

    def __str__(self):
        return f"Theme: {self.party}"


def _hex_to_rgb(hex_code: str) -> str | None:
    hex_code = hex_code.replace("#", "")

    if len(hex_code) != 6:
        return None

    # Convert the hex string to integer RGB values
    rgb = " ".join(
        [str(x) for x in list(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))]
    )
    return rgb
