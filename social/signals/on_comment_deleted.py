"""

"""

import logging

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from social.models import Comment

log = logging.getLogger(__name__)


@receiver(
    pre_delete,
    sender=Comment,
    dispatch_uid='create_placeholder_on_comment_deleted'
)
def create_placeholder_on_comment_deleted(sender, instance, using, **kwargs):
    instance.create_placeholder()
