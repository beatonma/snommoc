from django.db import models

from repository.models.mixins import (
    BaseModel,
    PeriodMixin,
)


class MessageOfTheDay(PeriodMixin, BaseModel):
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=1024)
    action_url = models.URLField(null=True, blank=True)
    display = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'MOTDs'
        verbose_name = 'Message Of The Day'

    def __str__(self):
        return f'{self.title}{" - " + self.action_url if self.action_url else ""}'
