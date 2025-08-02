from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from repository.models.mixins import ParliamentDotUkMixin, PersonMixin
from util.strings import ellipsise


class RegisteredInterestCategory(BaseModel):
    codename_major = models.PositiveSmallIntegerField()
    codename_minor = models.CharField(max_length=5, null=True, blank=True)
    name = models.CharField(max_length=512)
    house = models.ForeignKey("House", on_delete=models.CASCADE)
    sort_order = models.PositiveSmallIntegerField(default=0)

    def codename(self):
        return "".join(
            [str(x) for x in (self.codename_major, self.codename_minor) if x]
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Registered interest categories")
        constraints = (
            models.UniqueConstraint(
                fields=("codename_major", "codename_minor", "house"),
                name="unique_codename_per_house",
            ),
        )
        ordering = (
            "house",
            "sort_order",
        )


class RegisteredInterest(
    ParliamentDotUkMixin,
    PersonMixin,
    BaseModel,
):
    """Declared investments/involvements/relationships that a person has with
    organisations that could potentially influence their work in Parliament."""

    parliamentdotuk = models.PositiveIntegerField(
        help_text=_("ID used on parliament.uk website - unique per person")
    )  # *Not* unique globally or even per category. Not clear what the intended scope is!
    category = models.ForeignKey("RegisteredInterestCategory", on_delete=models.CASCADE)
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="registered_interests",
    )
    description = models.TextField()
    description_data = models.JSONField(default=dict)

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

    def _dev_reparse_description(self):
        from crawlers.parliamentdotuk.tasks.openapi.members.schema.registeredinterest import (
            _parse_description,
        )

        parsed = _parse_description(self.description)
        self.description_data = parsed.model_dump(mode="json")
        self.save(update_fields=["description_data"])

    def __str__(self):
        return f"{self.person}: {ellipsise(self.description)}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("parliamentdotuk", "person"), name="unique_id_per_person"
            )
        ]
        ordering = ("-amended", "-created")
