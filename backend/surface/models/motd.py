from datetime import date

from django.db import models
from django.db.models import Q
from repository.models.mixins import BaseModel, PeriodMixin, PeriodQuerySet


class MotdQuerySet(PeriodQuerySet):
    def filter_date(self, dt: date):
        return self.filter(
            Q(display=True)
            & (Q(start__isnull=True) | Q(start__lte=dt))
            & (Q(end__isnull=True) | Q(end__gte=dt))
        )


class MessageOfTheDay(PeriodMixin, BaseModel):
    objects = MotdQuerySet.as_manager()

    title = models.CharField(max_length=512)
    description = models.CharField(max_length=1024)
    action_url = models.URLField(null=True, blank=True)
    display = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "MOTDs"
        verbose_name = "Message Of The Day"

    def __str__(self):
        return f'{self.title}{" - " + self.action_url if self.action_url else ""}'
