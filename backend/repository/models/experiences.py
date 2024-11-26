from common.models import BaseModel
from django.db import models
from repository.models.mixins import ParliamentDotUkMixin, PeriodMixin, PersonMixin


class ExperienceCategory(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Experience categories"


class Experience(PersonMixin, PeriodMixin, ParliamentDotUkMixin, BaseModel):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    category = models.ForeignKey(
        "ExperienceCategory",
        on_delete=models.CASCADE,
    )

    organisation = models.ForeignKey(
        "Organisation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.category} {self.title}@{self.organisation}"
