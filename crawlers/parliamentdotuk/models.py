import traceback

from django.db import models

from repository.models.mixins import BaseModel


class UpdateError(BaseModel):
    parliamentdotuk = models.PositiveIntegerField()
    error_message = models.TextField(default="")
    trace = models.TextField(default="")
    handled = models.BooleanField(default=False)

    @classmethod
    def create(cls, parliamentdotuk: int, error):
        cls.objects.create(
            parliamentdotuk=parliamentdotuk,
            error_message=str(error),
            trace=traceback.format_exc(limit=20),
        )

    class Meta:
        abstract = True


class BillUpdateError(UpdateError):
    class Meta:
        verbose_name_plural = "BillUpdateErrors"
        verbose_name = "BillUpdateError"

    def __str__(self):
        return f"Bill {self.parliamentdotuk}"


class CommonsDivisionUpdateError(UpdateError):
    class Meta:
        verbose_name_plural = "CommonsDivisionUpdateErrors"
        verbose_name = "CommonsDivisionUpdateError"

    def __str__(self):
        return f"Commons Division {self.parliamentdotuk}"


class LordsDivisionUpdateError(UpdateError):
    class Meta:
        verbose_name_plural = "LordsDivisionUpdateErrors"
        verbose_name = "LordsDivisionUpdateError"

    def __str__(self):
        return f"Lords Division {self.parliamentdotuk}"


class ElectionResultUpdateError(UpdateError):
    class Meta:
        verbose_name_plural = "ElectionResult Update Errors"
        verbose_name = "ElectionResult Update Error"

    def __str__(self):
        return f"{self.parliamentdotuk}"
