"""

"""

import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

log = logging.getLogger(__name__)


class UserMixin(models.Model):
    user = models.ForeignKey(
        'UserToken',
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        abstract = True


class GenericTargetMixin(models.Model):
    target_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_type', 'target_id')

    class Meta:
        abstract = True


def get_target_kwargs(target: GenericTargetMixin) -> dict:
    return {
        'target_type': ContentType.objects.get_for_model(target),
        'target_id': target.pk,
    }
