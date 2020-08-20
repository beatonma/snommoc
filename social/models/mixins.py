"""

"""

import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

log = logging.getLogger(__name__)


class UserMixin(models.Model):
    user = models.ForeignKey(
        'UserToken',
        null=True,
        on_delete=models.SET_NULL,
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


class DeletionPendingMixin:
    """
    Mixin for models that may be deleted by a user.

    When deletion is requested, the instance should be marked
    as pending_deletion=True. The instance will no longer be available
    to public requests but will persist for a period of up to
    DELETION_PENDING_PERIOD_DAYS days to allow review by admins for potential
    abuse (e.g. posting abusive comments then deleting/remaking account), or
    to allow the user to request the instance be restored.

    After that period, the content will be irreversibly deleted.
    """
    DELETION_PENDING_PERIOD_DAYS = 14

    pending_deletion = models.BooleanField(default=False)
    deletion_requested = models.DateTimeField(
        null=True,
        blank=True,
        default=None
    )

    def mark_pending_deletion(self):
        self.pending_deletion = True
        self.deletion_requested = timezone.now()

    def is_expired(self):
        now = timezone.now()
        return (now - self.deletion_requested).days > DeletionPendingMixin.DELETION_PENDING_PERIOD_DAYS

    def create_placeholder(self):
        """Create an 'empty' version of this instance to stand in place of
        the deleted content. e.g. An empty comment with the timestamps of the
        original, a 'deleted' user account..."""
        pass


def get_target_kwargs(target: models.Model) -> dict:
    return {
        'target_type': ContentType.objects.get_for_model(target),
        'target_id': target.pk,
    }
