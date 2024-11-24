from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from repository.models.mixins import BaseModel, ParliamentDotUkMixin, PersonMixin


class AddressType(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)


class BaseAddress(PersonMixin, BaseModel):
    type = models.ForeignKey(
        "AddressType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_preferred = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.person} {self.type}"

    class Meta:
        abstract = True


class PhysicalAddress(BaseAddress):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="physical_addresses",
    )
    address = models.TextField(null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    fax = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Physical addresses"
        constraints = [
            models.UniqueConstraint(
                fields=["type", "person"],
                name="unique_address_type_per_person",
            )
        ]


class WebAddress(BaseAddress):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="web_addresses",
    )
    url = models.URLField()

    class Meta:
        verbose_name_plural = "Web addresses"
        constraints = [
            models.UniqueConstraint(
                fields=["type", "person"],
                name="unique_webaddress_type_per_person",
            )
        ]
