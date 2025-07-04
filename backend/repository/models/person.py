from typing import Optional, Self, Union, cast

from common.models import BaseModel, BaseQuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS
from repository.models.mixins import (
    AsciiNameMixin,
    ParliamentDotUkMixin,
    PeriodMixin,
    PersonMixin,
    SocialMixin,
    TheyWorkForYouMixin,
    WikipediaMixin,
)
from util import time as timeutil
from util.strings import get_similarity_score

NAME_MAX_LENGTH = 128


class PersonQuerySet(BaseQuerySet):
    def resolve(
        self,
        parliamentdotuk: int,
        name: str | None = None,
        defaults: dict | None = None,
    ):
        """Safely get the member with the given parliamentdotuk ID, or create
        it with given data if it does not already exist."""
        defaults = defaults or {}

        member, _ = self.get_or_create(
            parliamentdotuk=parliamentdotuk,
            defaults={
                "name": (name or "__UNKNOWN_MEMBER__"),
                **(defaults or {}),
            },
        )
        return member

    def filter(self, *args, **kwargs) -> Self:
        return cast("PersonQuerySet", super().filter(*args, **kwargs))

    def _filter_name(self, name: str) -> Self:
        return self.filter(Q(name__iexact=name) | Q(ascii_name__iexact=name))

    def search(self, query: str) -> Self:
        query = query.strip()
        return self.filter(
            Q(name__icontains=query)
            | Q(ascii_name__icontains=query)
            | Q(constituency__name__icontains=query)
        )

    def current(self) -> Self:
        return self.filter(status__is_current=True)

    def historical(self) -> Self:
        return self.filter(status__is_current=False)

    def active(self) -> Self:
        return self.filter(status__is_active=True)

    def inactive(self) -> Self:
        return self.current().filter(status__is_active=False)

    def for_house(self, house: str) -> Self:
        return self.filter(house__name__iexact=house)

    def for_party_id(self, party_id: int) -> Self:
        from repository.models.party import PartyQuerySet

        return self.filter(PartyQuerySet.reverse_party_id(party_id))

    def get_for_constituency(
        self, name: str, constituency_name: str, similarity_threshold: int = 60
    ) -> Union["Person", None]:
        """Try to find a Person with the given name who has a known relationship with the given constituency.

        similarity_threshold should be an integer between 0 and 100"""

        qs = self._filter_name(name).filter(constituency__name=constituency_name)
        if qs.count() == 1:
            return qs.first()

        qs = self._filter_name(name).prefetch_related("constituencies__constituency")
        potential = []

        def _safename(obj):
            return obj.name if obj else None

        for person in qs:
            constituencies_names = [_safename(person.constituency_or_none())] + [
                x.constituency.name for x in person.constituencies.all()
            ]
            for c in constituencies_names:
                similarity = get_similarity_score(c, constituency_name)
                if similarity >= similarity_threshold:
                    potential.append(person)

        if len(potential) == 1:
            return potential[0]


class Person(
    SocialMixin,
    ParliamentDotUkMixin,
    TheyWorkForYouMixin,
    WikipediaMixin,
    AsciiNameMixin,
    BaseModel,
):
    objects = PersonQuerySet.as_manager()
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text=_("Canonical name for this person."),
    )
    sort_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        null=True,
        blank=True,
        db_index=True,
    )

    full_title = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text=_("Official name with honorifics."),
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
        related_name="lords",
        related_query_name="lord",
        null=True,
        blank=True,
        default=None,
        help_text=_(
            "The source of this person's lordship, if applicable (e.g. hereditary, bishop, peerage, etc)"
        ),
    )

    party = models.ForeignKey(
        "Party",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            "Current party membership. Historic memberships can be retrieved via PartyAffiliation model."
        ),
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

    def constituency_or_none(self):
        try:
            return self.constituency
        except ObjectDoesNotExist:
            return None

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

    def save(self, *args, **kwargs):
        self.update_ascii_name(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} [{self.parliamentdotuk}]"

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("People")


class PersonStatus(PersonMixin, PeriodMixin, BaseModel):
    person = models.OneToOneField(
        "Person",
        on_delete=models.CASCADE,
        related_name="status",
    )
    is_current = models.BooleanField(
        db_index=True,
        help_text=_("Whether this person currently has a seat in one of the houses."),
    )
    is_active = models.BooleanField(
        db_index=True,
        help_text=_(
            "Whether this person is currently using their seat. May be false if they are on leave or suspended in some way."
        ),
    )
    description = models.TextField(null=True, blank=True)
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
        verbose_name_plural = _("People also known as")
        verbose_name = _("PersonAlsoKnownAs")

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
