from common.models import BaseModel
from django.db import models
from repository.models.mixins import PeriodMixin


class BaseFeatured(PeriodMixin, BaseModel):
    """Use start/end to define a period during which the item is featured."""

    target = None

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.target}: {self.start} -> {self.end}"


class FeaturedPerson(BaseFeatured):
    target = models.ForeignKey(
        "repository.Person",
        on_delete=models.CASCADE,
        related_name="+",
    )


class FeaturedBill(BaseFeatured):
    target = models.ForeignKey(
        "repository.Bill",
        on_delete=models.CASCADE,
        related_name="+",
    )


class FeaturedCommonsDivision(BaseFeatured):
    target = models.ForeignKey(
        "repository.CommonsDivision",
        on_delete=models.CASCADE,
        related_name="+",
    )


class FeaturedLordsDivision(BaseFeatured):
    target = models.ForeignKey(
        "repository.LordsDivision",
        on_delete=models.CASCADE,
        related_name="+",
    )
