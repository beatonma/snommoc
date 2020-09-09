"""
Simple wrapper classes for social targets, created to mark a target as being
recently engaged with - i.e. someone commented or voted on them.

These models should be used for caching - create/delete them on a short schedule
to represent engagement in the last hour or whatever.
"""

import logging

from django.db import models

from repository.models.mixins import BaseModel

log = logging.getLogger(__name__)


class RecentPersonEngagement(BaseModel):
    person = models.ForeignKey(
        'repository.Person',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'RecentMemberEngagements'
        verbose_name = 'RecentMemberEngagement'

    def __str__(self):
        return f'{self.person.name}'


class RecentCommonsDivisionEngagement(BaseModel):
    division = models.ForeignKey(
        'repository.CommonsDivision',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'RecentCommonsDivisionEngagements'
        verbose_name = 'RecentCommonsDivisionEngagement'

    def __str__(self):
        return f'{self.division.title}'


class RecentLordsDivisionEngagement(BaseModel):
    division = models.ForeignKey(
        'repository.LordsDivision',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'RecentLordsDivisionEngagements'
        verbose_name = 'RecentLordsDivisionEngagement'

    def __str__(self):
        return f'{self.division.title}'


class RecentBillEngagement(BaseModel):
    bill = models.ForeignKey(
        'repository.Bill',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'RecentBillEngagements'
        verbose_name = 'RecentBillEngagement'

    def __str__(self):
        return f'{self.bill.title}'
