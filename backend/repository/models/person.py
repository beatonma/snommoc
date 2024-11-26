from typing import Optional, cast

from common.models import BaseModel, BaseQuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS
from repository.models.mixins import (
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

    def filter(self, *args, **kwargs) -> "PersonQuerySet":
        return cast("PersonQuerySet", super().filter(*args, **kwargs))

    def filter_name(self, name: str):
        return self.filter(Q(name__iexact=name) | Q(aliases__alias__iexact=name))

    def active(self) -> "PersonQuerySet":
        return self.filter(status__is_active=True)

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
        help_text="Current party membership. Historic memberships can be retrieved via PartyAssociation model.",
    )

    house = models.ForeignKey(
        "House",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def is_active(self) -> bool:
        try:
            return self.status.is_active
        except ObjectDoesNotExist:
            return False

    def current_posts_qs(self):
        from repository.models.posts import PostHolder

        return PostHolder.objects.filter(person=self, end__isnull=True).order_by(
            "-start"
        )

    def current_posts(self):
        return self.current_posts_qs().values_list("post__name", flat=True)

    def age(self) -> int:
        if self.date_of_death:
            return timeutil.years_between(self.date_of_birth, self.date_of_death)
        else:
            return timeutil.years_since(self.date_of_birth)

    def is_birthday(self) -> bool:
        return timeutil.is_anniversary(self.date_of_birth)

    def is_mp(self) -> bool:
        if self.house:
            return self.is_active() and self.house.name == HOUSE_OF_COMMONS
        return False

    def is_lord(self) -> bool:
        if self.house:
            return self.is_active() and self.house.name == HOUSE_OF_LORDS
        return False

    def portrait_thumbnail_url(self) -> Optional[str]:
        try:
            return self.memberportrait.square_url
        except (AttributeError, ObjectDoesNotExist):
            pass

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


class PersonStatus(PersonMixin, PeriodMixin, BaseModel):
    person = models.OneToOneField(
        "Person",
        on_delete=models.CASCADE,
        related_name="status",
    )
    is_active = models.BooleanField(db_index=True)
    description = models.CharField(max_length=64, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return _("Active") if self.is_active else _("Inactive")


class PersonAlsoKnownAs(PersonMixin, BaseModel):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="aliases",
    )
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
