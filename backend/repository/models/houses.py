from typing import Literal

from common.models import BaseModel, BaseQuerySet
from django.db import models
from repository.models.mixins import PeriodMixin, PersonMixin

type HouseType = Literal["Commons", "Lords"]
HOUSE_OF_COMMONS: HouseType = "Commons"
HOUSE_OF_LORDS: HouseType = "Lords"


class HouseQuerySet(BaseQuerySet):
    def commons(self) -> "House":
        return self.get(name=HOUSE_OF_COMMONS)

    def lords(self) -> "House":
        return self.get(name=HOUSE_OF_LORDS)


class House(BaseModel):
    objects = HouseQuerySet.as_manager()
    name = models.CharField(
        max_length=16,
        unique=True,
    )

    def __str__(self):
        return self.name


class HouseMembership(PersonMixin, PeriodMixin, BaseModel):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="house_memberships",
    )
    house = models.ForeignKey(
        "House",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.house}: {self.person}"

    class Meta:
        unique_together = [
            ["start", "house", "person"],
        ]
