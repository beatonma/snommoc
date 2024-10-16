from django.db import models

from repository.models.mixins import BaseModel
from social.models.mixins import GenericTargetMixin


class ZeitgeistItem(GenericTargetMixin, BaseModel):
    REASON_FEATURE = "feature"
    REASON_SOCIAL = "social"

    """
    Represents something that is important now, because of social interaction
    or they have been featured.
    """
    reason = models.CharField(
        max_length=24,
        choices=[
            (REASON_FEATURE, REASON_FEATURE),
            (REASON_SOCIAL, REASON_SOCIAL),
        ],
    )

    """
    Optional value to make an item more or less prominent in UIs. Higher value indicate higher importance.
    Items with equal priority may be displayed in any order.
    """
    priority = models.PositiveSmallIntegerField(default=50)

    class Meta:
        verbose_name_plural = "Zeitgeist items"
        verbose_name = "Zeitgeist item"
        unique_together = [
            ["target_id", "target_type"],
        ]

    def __str__(self):
        return f"{self.target} [{self.reason}]"
