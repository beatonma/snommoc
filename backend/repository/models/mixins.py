import datetime
from datetime import date

from common.models import BaseQuerySet
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from util.time import in_range, is_current


class UnresolvedQuerySet(BaseQuerySet):
    """A queryset for models which have fields that may not be set automatically.

    e.g. A model has a Person foreign key but its source data does not include
    an ID so the Person cannot be created and may not be resolved from available data.
    """

    def unresolved(self):
        """Returns a queryset whose entries have unresolved values."""
        raise NotImplementedError(
            f"{self.__class__.__name__}.unresolved() has not been implemented"
        )


class PersonMixin(models.Model):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class PeriodQuerySet(BaseQuerySet):
    def filter_date_range(self, start: date | None, end: date | None):
        return self.filter(
            (Q(start__isnull=True) | Q(start__lte=end))
            & (Q(end__isnull=True) | Q(end__gte=start))
        )

    def filter_date(self, dt: date):
        return self.filter_date_range(dt, dt)

    def filter_current(self):
        return self.filter(end__isnull=True)


class PeriodMixin(models.Model):
    """For models that represent something with a start/end date"""

    objects = PeriodQuerySet.as_manager()
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    def is_current(self) -> bool:
        return is_current(self.start, self.end)

    def contains(self, other_date: datetime.date) -> bool:
        return in_range(other_date, self.start, self.end)

    def describe_timespan(self) -> str:
        if self.start and self.end:
            return f"{self.start} - {self.end}"
        if self.start:
            return f"since {self.start}"
        return ""

    @staticmethod
    def meta_ordering_recent():
        return ["-end", "-start"]

    class Meta:
        abstract = True


class ParliamentDotUkMixin(models.Model):
    """For models that have a corresponding api on parliament.uk"""

    parliamentdotuk = models.PositiveIntegerField(
        primary_key=True, unique=True, help_text=_("ID used on parliament.uk website")
    )

    class Meta:
        abstract = True


class TheyWorkForYouMixin(models.Model):
    """For models that have a corresponding api on theyworkforyou.com"""

    theyworkforyou = models.PositiveIntegerField(
        unique=True, null=True, help_text=_("ID used on theyworkforyou.com")
    )

    class Meta:
        abstract = True


class WikipediaMixin(models.Model):
    wikipedia = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text=_("Path section of a wikipedia url (e.g. 'John_Baron_(politician)')"),
    )

    class Meta:
        abstract = True


class SocialMixin:
    def social_title(self) -> str:
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement method social_title()"
        )


class AsciiNameMixin(models.Model):
    ascii_name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("Simplified ASCII name"),
    )

    def update_ascii_name(self, source: str):
        if not self.ascii_name:
            ascii_name = self.normalize_ascii(source)
            if ascii_name != source:
                self.ascii_name = ascii_name

    @staticmethod
    def normalize_ascii(value: str) -> str:
        import unicodedata

        return (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )

    class Meta:
        abstract = True
