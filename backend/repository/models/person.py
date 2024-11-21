from typing import Optional, cast

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS
from repository.models.mixins import (
    BaseModel,
    BaseQuerySet,
    ParliamentDotUkMixin,
    PeriodMixin,
    PersonMixin,
    SocialMixin,
    TheyWorkForYouMixin,
    WikipediaMixin,
)
from util import time as timeutil

NAME_MAX_LENGTH = 128


class PersonQuerySet(BaseQuerySet):
    def get_member(
        self,
        parliamentdotuk: int,
        name: str | None = None,
        defaults: dict | None = None,
    ):
        """Safely get the member with the given parliamentdotuk ID, or create
        it with given data if it does not already exist."""
        member, _ = self.get_or_create(
            parliamentdotuk=parliamentdotuk,
            defaults={"name": name or "__UNKNOWN_MEMBER__", **(defaults or {})},
        )
        return member

    def filter_name(self, name: str):
        return self.filter(
            Q(name__iexact=name) | Q(personalsoknownas__alias__iexact=name)
        )

    def filter(self, *args, **kwargs) -> "PersonQuerySet":
        return cast("PersonQuerySet", super().filter(*args, **kwargs))

    def active(self) -> "PersonQuerySet":
        return self.filter(active=True)

    def commons(self) -> "PersonQuerySet":
        return self.filter(house__name=HOUSE_OF_COMMONS)

    def lords(self) -> "PersonQuerySet":
        return self.filter(house__name=HOUSE_OF_LORDS)


class Person(
    SocialMixin,
    ParliamentDotUkMixin,
    TheyWorkForYouMixin,
    WikipediaMixin,
    BaseModel,
):
    objects = PersonQuerySet.as_manager()
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text="Canonical name for this person.",
    )
    given_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text="First name",
        null=True,
        blank=True,
    )
    family_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text="Last name",
        null=True,
        blank=True,
    )
    additional_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text="Middle name(s)",
        blank=True,
        null=True,
    )

    full_title = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text="Official name with honorifics.",
        blank=True,
        null=True,
    )

    gender = models.CharField(
        max_length=16,
        default=None,
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        default=None,
        null=True,
        blank=True,
    )
    date_of_death = models.DateField(
        default=None,
        null=True,
        blank=True,
    )

    town_of_birth = models.ForeignKey(
        "Town",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    country_of_birth = models.ForeignKey(
        "Country",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    lords_type = models.ForeignKey(
        "LordsType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        help_text="The source of this person's lordship, if applicable (e.g. hereditary, bishop, peerage, etc)",
    )

    party = models.ForeignKey(
        "Party",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Current party membership. Historic memberships can be "
        "retrieved via PartyAssociation model.",
    )

    house = models.ForeignKey(
        "House",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_entered_house = models.DateField(
        default=None,
        null=True,
        blank=True,
    )
    date_left_house = models.DateField(
        default=None,
        null=True,
        blank=True,
    )
    active = models.BooleanField(
        default=False,
        help_text="Whether this person currently has a seat in parliament.",
    )

    current_post = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default=None,
    )

    @property
    def age(self) -> int:
        if self.date_of_death:
            return timeutil.years_between(self.date_of_birth, self.date_of_death)
        else:
            return timeutil.years_since(self.date_of_birth)

    @property
    def is_birthday(self) -> bool:
        return timeutil.is_anniversary(self.date_of_birth)

    @property
    def is_mp(self) -> bool:
        if self.house:
            return self.active and self.house.name == HOUSE_OF_COMMONS
        return False

    @property
    def is_lord(self) -> bool:
        if self.house:
            return self.active and self.house.name == HOUSE_OF_LORDS
        return False

    @property
    def portrait_thumbnail_url(self) -> Optional[str]:
        try:
            return self.memberportrait.square_url
        except (AttributeError, ObjectDoesNotExist):
            pass

    @property
    def portrait_fullsize_url(self) -> Optional[str]:
        try:
            return self.memberportrait.fullsize_url
        except (AttributeError, ObjectDoesNotExist):
            pass

    def social_title(self) -> str:
        return self.name

    def __str__(self):
        return f"{self.name} [{self.parliamentdotuk}]"

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "People"


class PersonAlsoKnownAs(PersonMixin, BaseModel):
    alias = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name_plural = "People also known as"
        verbose_name = "PersonAlsoKnownAs"

    def __str__(self):
        return f"{self.alias} -> {self.person}"


class LifeEvent(PeriodMixin, PersonMixin):
    """
    [UNUSED]
    Miscellaneous additional data about an event in a Person's life.
    e.g. Graduations? Marriage/significant relationships? Arrests?

    If this is used in future, would likely need to be maintained manually - could potentially be done through wiki-like
    crowd-sourcing but that brings potential issues with significance/neutrality/sourcing/moderation/truth.
    """

    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
