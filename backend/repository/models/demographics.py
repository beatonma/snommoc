from common.models import BaseModel
from django.db import models


class PartyDemographics(BaseModel):
    party = models.ForeignKey(
        "Party",
        on_delete=models.CASCADE,
        related_name="demographics",
    )
    house = models.ForeignKey(
        "House",
        on_delete=models.CASCADE,
        related_name="demographics",
    )

    male_member_count = models.PositiveSmallIntegerField()
    female_member_count = models.PositiveSmallIntegerField()
    non_binary_member_count = models.PositiveSmallIntegerField()
    total_member_count = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["party", "house"],
                name="unique_demographics_per_party_per_house",
            ),
        ]

    def __str__(self):
        return f"{self.party.name} {self.house.name}"


class LordsDemographics(BaseModel):
    party = models.OneToOneField(
        "Party",
        on_delete=models.CASCADE,
        related_name="lords_demographics",
    )

    life_count = models.PositiveSmallIntegerField()
    hereditary_count = models.PositiveSmallIntegerField()
    bishop_count = models.PositiveSmallIntegerField()
    total_count = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.party.name
