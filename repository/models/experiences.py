from django.db import models

from repository.models.mixins import (
    BaseModel,
    PeriodMixin,
    PersonMixin,
)


class ExperienceCategory(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Experience categories"


class Experience(PersonMixin, PeriodMixin, BaseModel):
    category = models.ForeignKey(
        "ExperienceCategory",
        on_delete=models.CASCADE,
    )

    organisation = models.CharField(max_length=512, null=True, blank=True)
    title = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.category} {self.title}@{self.organisation}"
