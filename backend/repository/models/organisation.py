import re

from django.db import models
from django.utils.text import slugify

from common.models import BaseModel, BaseQuerySet


class OrganisationQuerySet(BaseQuerySet):
    def get(self, *args, **kwargs):
        kwargs = self._normalise(kwargs)

        if name := kwargs.get("name"):
            slug = Organisation.slugify(name)
            existing = self.filter(slug=slug)
            if existing.exists():
                return existing.first()

        return super().get(*args, **kwargs)

    def get_or_create(self, defaults=None, **kwargs):
        defaults = self._normalise(defaults)
        kwargs = self._normalise(kwargs)

        name: str | None = (defaults.get("name") if defaults else None) or (
            kwargs.get("name") if kwargs else None
        )
        if name:
            slug = Organisation.slugify(name)
            existing = self.filter(slug=slug)
            if existing.exists():
                return existing.first(), False

        return super().get_or_create(defaults=defaults, **kwargs)

    def search(self, query: str):
        return self.filter(name__icontains=query)

    @staticmethod
    def _normalise(obj: dict | None):
        if obj and "name" in obj:
            obj["name"] = Organisation.normalise_name(obj["name"])

        return obj


class Organisation(BaseModel):
    objects = OrganisationQuerySet.as_manager()
    name = models.CharField(max_length=512, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    url = models.URLField(null=True, blank=True)
    companies_house_id = models.CharField(
        max_length=64, unique=True, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = self.slugify(self.name)
        super().save(*args, **kwargs)

    @classmethod
    def slugify(cls, text: str):
        return slugify(text[:50])

    @classmethod
    def normalise_name(cls, name: str):
        def _titlecase_with_acronyms(match):
            word: str = match[0]
            if re.fullmatch(r"([A-Z]\.?){2,}", word):
                # Remove dot separators from acronyms
                return word.replace(".", "")
            if re.fullmatch(r"(of|the|an?|to)", word):
                return word
            return word.capitalize()

        name = name.replace(" and ", " & ")
        name = re.sub(r"[.\w]+", _titlecase_with_acronyms, name)
        name = re.sub(r"\bPLC\b", "PLC", name, flags=re.IGNORECASE)
        name = re.sub(r"\bLtd\b\.?", "Ltd", name, flags=re.IGNORECASE)
        name = re.sub(r"\bDept\b\.?", "Department", name, flags=re.IGNORECASE)
        name = re.sub(r"(\d),", r"\g<1>", name)
        return name

    def __str__(self):
        return f"{self.name} [{self.url}]"

    class Meta:
        ordering = ["name"]
