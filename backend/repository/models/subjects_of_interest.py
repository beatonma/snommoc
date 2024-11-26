from common.models import BaseModel
from django.db import models
from repository.models.mixins import PersonMixin


class SubjectOfInterestCategory(BaseModel):
    title = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = "Subject of interest categories"


class SubjectOfInterest(PersonMixin, BaseModel):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="subjects_of_interest",
    )
    category = models.ForeignKey("SubjectOfInterestCategory", on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Subjects of interest"

    def __str__(self):
        return f"[{self.category.title}] {self.description}"
