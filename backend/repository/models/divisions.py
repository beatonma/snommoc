from common.models import BaseModel, BaseQuerySet
from django.db import models
from django.db.models import UniqueConstraint
from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS
from repository.models.mixins import ParliamentDotUkMixin, SocialMixin


class DivisionSharedProperties(SocialMixin, models.Model):
    title: models.CharField
    date: models.DateField
    house: str
    ayes: int
    noes: int
    is_passed: bool

    def social_title(self) -> str:
        return str(self.title)

    class Meta:
        abstract = True


class CommonsDivision(DivisionSharedProperties, ParliamentDotUkMixin, BaseModel):
    title = models.CharField(max_length=512)
    date = models.DateField()

    session = models.ForeignKey(
        "ParliamentarySession",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    division_number = models.PositiveSmallIntegerField()

    ayes = models.PositiveSmallIntegerField(
        help_text="How many members voted for the motion",
    )
    noes = models.PositiveSmallIntegerField(
        help_text="How many members voted against the motion",
    )
    did_not_vote = models.PositiveSmallIntegerField(
        help_text="How many members did not vote at all"
    )
    is_deferred_vote = models.BooleanField(
        default=False,
        help_text="A deferred vote is one that is not held immediately "
        "at the end of the debate, but at a later 'convenient' time",
    )
    is_passed = models.BooleanField()

    @staticmethod
    def house():
        return HOUSE_OF_COMMONS

    def margin(self) -> int:
        return abs(self.ayes - self.noes)

    def __str__(self):
        return self.title


class LordsDivision(DivisionSharedProperties, ParliamentDotUkMixin, BaseModel):
    title = models.TextField(null=True, blank=True)
    date = models.DateField()
    number = models.PositiveSmallIntegerField()
    amendment_motion_notes = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    is_whipped = models.BooleanField()
    is_government_content = models.BooleanField()
    authoritative_content_count = models.PositiveSmallIntegerField()
    authoritative_not_content_count = models.PositiveSmallIntegerField()
    division_had_tellers = models.BooleanField()
    teller_content_count = models.PositiveSmallIntegerField()
    teller_not_content_count = models.PositiveSmallIntegerField()
    member_content_count = models.PositiveSmallIntegerField()
    member_not_content_count = models.PositiveSmallIntegerField()
    sponsoring_member = models.ForeignKey(
        "repository.Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sponsored_lords_divisions",
    )
    is_house = models.BooleanField(null=True)
    is_passed = models.BooleanField()
    is_government_win = models.BooleanField(null=True, blank=True)

    @staticmethod
    def house() -> str:
        return HOUSE_OF_LORDS

    @property
    def ayes(self) -> int:
        return self.authoritative_content_count

    @property
    def noes(self) -> int:
        return self.authoritative_not_content_count

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
            .order_by("division__date")
        )


class DivisionVoteSharedProperties(models.Model):
    person: models.ForeignKey
    division: models.ForeignKey
    vote_type: models.ForeignKey

    class Meta:
        abstract = True


def _base_DivisionVote(*, division_fk: str, person_related_name: str):
    """Generate abstract base class for CommonsDivisionVote,LordsDivisionVote

    Args:
        division_fk: ForeignKey `to` value for `division` field.
        person_related_name: `related_name` for `person` field.
    """

    class _DivisionVote(DivisionVoteSharedProperties, BaseModel):
        objects = DivisionVoteQuerySet.as_manager()

        person = models.ForeignKey(
            "repository.Person",
            on_delete=models.CASCADE,
            related_name=person_related_name,
        )
        division = models.ForeignKey(
            division_fk,
            on_delete=models.CASCADE,
            related_name="votes",
        )
        vote_type = models.ForeignKey(
            "repository.DivisionVoteType",
            on_delete=models.CASCADE,
            related_name="+",
            null=True,
        )
        is_teller = models.BooleanField(default=False)

        class Meta:
            abstract = True
            constraints = [
                UniqueConstraint(
                    fields=["person", "division"],
                    name=f"One vote per person per {division_fk}",
                ),
            ]
            ordering = [
                "-modified_at",
            ]

    return _DivisionVote


class LordsDivisionVote(
    _base_DivisionVote(
        division_fk="repository.LordsDivision",
        person_related_name="lords_votes",
    )
):
    pass


class CommonsDivisionVote(
    _base_DivisionVote(
        division_fk="repository.CommonsDivision",
        person_related_name="commons_votes",
    )
):
    pass
