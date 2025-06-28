from common.models import BaseModel, BaseQuerySet
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils.translation import gettext_lazy as _
from repository.models.event import ParliamentaryEvent
from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS
from repository.models.mixins import SocialMixin


class DivisionQuerySet(BaseQuerySet):
    def search(self, query: str):
        query = query.strip()

        return self.filter(title__icontains=query)


class Division(ParliamentaryEvent, SocialMixin, models.Model):
    objects = DivisionQuerySet.as_manager()

    parliamentdotuk = models.PositiveIntegerField(
        help_text=_("ID used on parliament.uk website")
    )
    house = models.ForeignKey("repository.House", on_delete=models.CASCADE)

    title = models.TextField(null=True, blank=True)
    is_passed = models.BooleanField()
    number = models.PositiveSmallIntegerField()

    ayes = models.PositiveSmallIntegerField(
        help_text=_("How many members voted for the motion"),
    )
    noes = models.PositiveSmallIntegerField(
        help_text=_("How many members voted against the motion"),
    )

    def social_title(self) -> str:
        return str(self.title)

    class Meta:

        constraints = [
            UniqueConstraint(
                fields=["parliamentdotuk", "house"],
                name=f"Unique id per house",
            ),
        ]


class CommonsDivision(Division, BaseModel):
    session = models.ForeignKey(
        "ParliamentarySession",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    did_not_vote = models.PositiveSmallIntegerField(
        help_text=_("How many members did not vote at all")
    )
    is_deferred_vote = models.BooleanField(
        default=False,
        help_text=_(
            "A deferred vote is one that is not held immediately "
            "at the end of the debate, but at a later 'convenient' time"
        ),
    )

    def margin(self) -> int:
        return abs(self.ayes - self.noes)

    def __str__(self):
        return self.title


class LordsDivision(Division, BaseModel):
    amendment_motion_notes = models.TextField(null=True, blank=True)
    is_whipped = models.BooleanField()
    is_government_content = models.BooleanField()
    division_had_tellers = models.BooleanField()
    teller_content_count = models.PositiveSmallIntegerField()
    teller_not_content_count = models.PositiveSmallIntegerField()
    sponsoring_member = models.ForeignKey(
        "repository.Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sponsored_lords_divisions",
    )
    is_government_win = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.date})"


class DivisionVoteType(BaseModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class DivisionVoteQuerySet(BaseQuerySet):
    def for_member(self, person):
        return (
            self.filter(person=person)
            .select_related("division")
            .order_by("-division__date")
        )

    def search(self, query: str):
        return self.filter(person__name__icontains=query)

    def by_type(self, vote_type: str):
        if vote_type == "aye" or vote_type == "content":
            return self.filter(Q(vote_type__name="aye") | Q(vote_type__name="content"))
        if vote_type == "no" or vote_type == "not_content":
            return self.filter(
                Q(vote_type__name="no") | Q(vote_type__name="not_content")
            )
        return self.filter(vote_type__name=vote_type)

    def commons(self, division_parliamentdotuk: int = None):
        qs = self.filter(division__house__name=HOUSE_OF_COMMONS)
        if division_parliamentdotuk:
            qs = qs.filter(division__parliamentdotuk=division_parliamentdotuk)
        return qs

    def lords(self, division_parliamentdotuk: int = None):
        qs = self.filter(division__house__name=HOUSE_OF_LORDS)
        if division_parliamentdotuk:
            qs = qs.filter(division__parliamentdotuk=division_parliamentdotuk)
        return qs


class DivisionVote(BaseModel):
    objects = DivisionVoteQuerySet.as_manager()
    person = models.ForeignKey(
        "repository.Person",
        on_delete=models.CASCADE,
        related_name="votes",
    )
    division = models.ForeignKey(
        "repository.Division",
        on_delete=models.CASCADE,
        related_name="votes",
    )
    vote_type = models.ForeignKey(
        "repository.DivisionVoteType",
        on_delete=models.CASCADE,
        related_name="+",
    )
    is_teller = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["person", "division"],
                name=f"One vote per person per division",
            ),
        ]
        ordering = [
            "-division__date",
        ]
