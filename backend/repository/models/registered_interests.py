from django.db import models
from repository.models.mixins import BaseModel, ParliamentDotUkMixin, PersonMixin


class RegisteredInterestCategory(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Registered interest categories"


class RegisteredInterest(
    ParliamentDotUkMixin,
    PersonMixin,
    BaseModel,
):
    """Declared investments/involvements/relationships that a person has with
    organisations that could potentially influence their work in Parliament."""

    parliamentdotuk = models.PositiveIntegerField(
        help_text="ID used on parliament.uk website - unique per person"
    )  # *Not* unique globally or even per category. Not clear what the intended scope is!
    category = models.ForeignKey("RegisteredInterestCategory", on_delete=models.CASCADE)
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="registered_interests",
    )
    description = models.TextField()

    created = models.DateField(blank=True, null=True)
    amended = models.DateField(blank=True, null=True)
    deleted = models.DateField(blank=True, null=True)
    is_correction = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "RegisteredInterest",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.person}: {self.description}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parliamentdotuk", "person"], name="unique_id_per_person"
            )
        ]
