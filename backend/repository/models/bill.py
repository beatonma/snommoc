from common.models import BaseModel
from django.db import models
from django.db.models import UniqueConstraint
from phonenumber_field.modelfields import PhoneNumberField
from repository.models.mixins import ParliamentDotUkMixin, SocialMixin
from util.strings import ellipsise


class BillStageType(ParliamentDotUkMixin, BaseModel):
    """Definition of a type of bill stage"""

    name = models.CharField(max_length=255)
    house = models.ForeignKey("repository.House", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BillStage(ParliamentDotUkMixin, BaseModel):
    """Represents a stage of a specific Bill.

    Based on StageSummary viewmodel from https://bills-api.parliament.uk/index.html"""

    bill = models.ForeignKey(
        "repository.Bill",
        on_delete=models.CASCADE,
        related_name="stages",
    )

    description = models.CharField(max_length=255, null=True, blank=True)
    abbreviation = models.CharField(max_length=16, null=True, blank=True)

    house = models.ForeignKey(
        "repository.House",
        on_delete=models.CASCADE,
        related_name="+",
    )

    stage_type = models.ForeignKey(
        "repository.BillStageType",
        on_delete=models.CASCADE,
        related_name="+",
    )

    session = models.ForeignKey(
        "repository.ParliamentarySession",
        on_delete=models.CASCADE,
        related_name="bill_stages",
    )

    sort_order = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.description}: {self.bill}"


class BillStageSitting(ParliamentDotUkMixin, BaseModel):
    stage = models.ForeignKey(
        "repository.BillStage",
        on_delete=models.CASCADE,
        related_name="sittings",
    )

    date = models.DateTimeField()

    def __str__(self):
        return f"{self.stage} [{self.date}]"

    class Meta:
        ordering = ["-date"]


class BillTypeCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BillType(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        "repository.BillTypeCategory",
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return self.name


class BillAgent(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class BillSponsor(BaseModel):
    bill = models.ForeignKey(
        "repository.Bill",
        on_delete=models.CASCADE,
        related_name="sponsors",
    )

    member = models.ForeignKey(
        "repository.Person",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sponsored_bills",
    )

    organisation = models.ForeignKey(
        "repository.Organisation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sponsored_bills",
    )

    sort_order = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.member}|{self.organisation}: {self.bill}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("bill", "member", "organisation"),
                name="unique_billsponsor_per_bill",
            )
        ]


class BillPublicationType(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return ellipsise(self.name)


class BillPublication(ParliamentDotUkMixin, BaseModel):
    bill = models.ForeignKey(
        "repository.Bill",
        on_delete=models.CASCADE,
        related_name="publications",
    )
    publication_type = models.ForeignKey(
        "repository.BillPublicationType",
        on_delete=models.CASCADE,
        related_name="+",
    )
    house = models.ForeignKey(
        "repository.House",
        on_delete=models.CASCADE,
        related_name="+",
    )
    title = models.TextField()
    display_date = models.DateTimeField()

    def __str__(self):
        return ellipsise(self.title)


class BillPublicationLink(ParliamentDotUkMixin, BaseModel):
    publication = models.ForeignKey(
        "repository.BillPublication",
        on_delete=models.CASCADE,
        related_name="links",
    )

    title = models.TextField()
    url = models.URLField(max_length=500)
    content_type = models.CharField(max_length=128)

    def __str__(self):
        return ellipsise(self.title)


class Bill(SocialMixin, ParliamentDotUkMixin, BaseModel):
    title = models.CharField(max_length=255)
    long_title = models.TextField(null=True, blank=True)
    summary = models.TextField(
        null=True, blank=True, help_text="HTML-formatted description"
    )

    current_house = models.ForeignKey(
        "repository.House",
        on_delete=models.CASCADE,
        related_name="bills_current",
    )
    originating_house = models.ForeignKey(
        "repository.House",
        on_delete=models.CASCADE,
        related_name="bills_originated",
    )
    last_update = models.DateTimeField()
    withdrawn_at = models.DateTimeField(null=True, blank=True)
    is_defeated = models.BooleanField()
    is_act = models.BooleanField()
    bill_type = models.ForeignKey(
        "repository.BillType",
        on_delete=models.CASCADE,
        related_name="+",
    )
    session_introduced = models.ForeignKey(
        "repository.ParliamentarySession",
        on_delete=models.CASCADE,
        related_name="bills_introduced",
    )
    sessions = models.ManyToManyField(
        "repository.ParliamentarySession",
        related_name="bills",
    )

    current_stage = models.ForeignKey(
        "repository.BillStage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )

    petitioning_period = models.CharField(max_length=512, null=True, blank=True)
    petitioning_information = models.TextField(null=True, blank=True)

    agent = models.ForeignKey(
        "repository.BillAgent",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    promoters = models.ManyToManyField(
        "repository.Organisation",
        related_name="promoted_bills",
    )

    def social_title(self) -> str:
        return self.title

    def __str__(self):
        return self.title
