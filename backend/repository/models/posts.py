from django.db import models
from django.utils.translation import gettext_lazy as _
from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
    PeriodMixin,
    PersonMixin,
)


class Post(ParliamentDotUkMixin, BaseModel):
    class PostType(models.TextChoices):
        GOVERNMENT = "government", _("Government")
        OPPOSITION = "opposition", _("Opposition")
        OTHER = "other", _("Other")

    type = models.CharField(max_length=24, choices=PostType.choices)
    name = models.CharField(max_length=512)
    hansard_name = models.CharField(
        max_length=512,
        null=True,
        blank=True,
    )
    additional_info = models.CharField(max_length=512, null=True, blank=True)
    additional_info_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class PostHolder(PersonMixin, PeriodMixin, BaseModel):
    """Base class representing a period of tenancy where the person held the post."""

    person = models.ForeignKey("Person", on_delete=models.CASCADE, related_name="posts")
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="holders",
    )
