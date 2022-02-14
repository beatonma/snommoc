from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
)


class BillStageType(ParliamentDotUkMixin, BaseModel):
    """Definition of a type of bill stage"""

    name = models.CharField(max_length=256)
    house = models.ForeignKey("repository.House", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BillStage(ParliamentDotUkMixin, BaseModel):
    """Represents a stage of a specific Bill.

    Based on StageSummary viewmodel from https://bills-api.parliament.uk/index.html"""

    bill = models.ForeignKey(
        "repository.Bill",
        on_delete=models.CASCADE,
    )

    description = models.CharField(max_length=256, null=True, blank=True)
    abbreviation = models.CharField(max_length=16, null=True, blank=True)

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


class BillTypeCategory(BaseModel):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class BillType(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=256)
    description = models.TextField()
    category = models.ForeignKey(
        "repository.BillTypeCategory",
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return self.name


class BillAgent(BaseModel):
    name = models.CharField(max_length=256)
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


class Bill(ParliamentDotUkMixin, BaseModel):
    short_title = models.CharField(max_length=512)
    long_title = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

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
    bill_withdrawn = models.DateTimeField(null=True, blank=True)
    is_defeated = models.BooleanField()
    is_act = models.BooleanField()
    bill_type = models.ForeignKey(
        "repository.BillType",
        on_delete=models.CASCADE,
        related_name="+",
    )
    introduced_session = models.ForeignKey(
        "repository.ParliamentarySession",
        on_delete=models.CASCADE,
        related_name="bills_introduced",
    )
    included_sessions = models.ManyToManyField(
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

    def __str__(self):
        return self.short_title
