"""

"""

import logging

from django.db import models

from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
)

log = logging.getLogger(__name__)


class BillType(BaseModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)


class BillSponsor(BaseModel):
    name = models.CharField(max_length=128, null=True, blank=True)
    person = models.ForeignKey(
        'Person',
        models.CASCADE,
        null=True,
    )
    bill = models.ForeignKey(
        'Bill',
        on_delete=models.CASCADE,
    )


class BillStageType(ParliamentDotUkMixin, BaseModel):
    name = models.CharField(max_length=512)


class BillStage(ParliamentDotUkMixin, BaseModel):
    bill = models.ForeignKey(
        'Bill',
        on_delete=models.DO_NOTHING,
    )

    session = models.ForeignKey(
        'ParliamentarySession',
        on_delete=models.CASCADE,
        related_name='+',
    )

    bill_stage_type = models.ForeignKey(
        'BillStageType',
        on_delete=models.DO_NOTHING,
    )


class BillStageSitting(ParliamentDotUkMixin, BaseModel):
    bill_stage = models.ForeignKey(
        'BillStage',
        on_delete=models.DO_NOTHING,
        related_name='sittings',
    )
    date = models.DateField()
    formal = models.BooleanField()
    provisional = models.BooleanField()


class BillPublication(ParliamentDotUkMixin, BaseModel):
    bill = models.ForeignKey(
        'Bill',
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(max_length=512)


class Bill(ParliamentDotUkMixin, BaseModel):
    """A proposal for a new law, or a proposal to change an existing law that
    is presented for debate before Parliament."""
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=1024)
    act_name = models.CharField(max_length=512)
    homepage = models.URLField()

    ballot_number = models.PositiveIntegerField(default=0)
    bill_chapter = models.PositiveIntegerField(default=0)

    is_private = models.BooleanField()

    bill_type = models.ForeignKey(
        'BillType',
        on_delete=models.CASCADE,
    )
    session = models.ForeignKey(
        'ParliamentarySession',
        on_delete=models.CASCADE,
        null=True,
        related_name='bills',
    )
