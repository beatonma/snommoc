from django.db import models

from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
)


class BillType(BaseModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.name}"


class BillSponsor(BaseModel):
    name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Raw name of the person if a Person instance cannot be found.",
    )
    person = models.ForeignKey(
        "Person",
        models.CASCADE,
        null=True,
    )
    bill = models.ForeignKey(
        "Bill",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = [
            ["person", "bill"],
        ]

    def __str__(self):
        return f"{self.bill}: {self.name if self.name else self.person}"


class BillStageType(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.name}"


class BillStage(ParliamentDotUkMixin, BaseModel):
    bill = models.ForeignKey(
        "Bill",
        on_delete=models.CASCADE,
    )

    session = models.ForeignKey(
        "ParliamentarySession",
        on_delete=models.CASCADE,
        related_name="+",
    )

    bill_stage_type = models.ForeignKey(
        "BillStageType",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.bill_stage_type}: {self.bill}"


class BillStageSitting(ParliamentDotUkMixin, BaseModel):
    bill_stage = models.ForeignKey(
        "BillStage",
        on_delete=models.CASCADE,
        related_name="sittings",
    )
    date = models.DateField(blank=True, null=True)
    formal = models.BooleanField()
    provisional = models.BooleanField()

    def __str__(self):
        return f"{self.date}: {self.bill_stage}"


class BillPublication(ParliamentDotUkMixin, BaseModel):
    bill = models.ForeignKey(
        "Bill",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.parliamentdotuk}: {self.title}"


class Bill(ParliamentDotUkMixin, BaseModel):
    """A proposal for a new law, or a proposal to change an existing law that
    is presented for debate before Parliament."""

    title = models.CharField(max_length=512)
    description = models.CharField(max_length=2048, null=True, blank=True)
    act_name = models.CharField(max_length=512, null=True, blank=True)
    label = models.CharField(max_length=512)
    homepage = models.URLField()
    date = models.DateField()

    ballot_number = models.PositiveIntegerField(default=0)
    bill_chapter = models.CharField(max_length=64, blank=True, null=True)

    is_private = models.BooleanField(default=False)
    is_money_bill = models.BooleanField(default=False)

    public_involvement_allowed = models.BooleanField(default=False)

    bill_type = models.ForeignKey(
        "BillType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    session = models.ForeignKey(
        "ParliamentarySession",
        on_delete=models.CASCADE,
        null=True,
        related_name="bills",
    )

    def __str__(self):
        return f"{self.parliamentdotuk}: {self.title}"
