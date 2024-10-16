from django.db import models

from repository.models.mixins import (
    BaseModel,
    PersonMixin,
)


class SubjectOfInterestCategory(BaseModel):
    title = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "Subject of interest categories"


class SubjectOfInterest(PersonMixin, BaseModel):
    """A subject that a person is particularly interested in.
    This is distinct from"""

    category = models.ForeignKey("SubjectOfInterestCategory", on_delete=models.CASCADE)

    subject = models.CharField(max_length=512)

    class Meta:
        verbose_name_plural = "Subjects of interest"

    def __str__(self):
        return f"[{self.category.title}] {self.subject}"
