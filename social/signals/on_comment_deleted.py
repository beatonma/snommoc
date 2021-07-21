from django.db.models.signals import pre_delete
from django.dispatch import receiver

from social.models import Comment


@receiver(
    pre_delete, sender=Comment, dispatch_uid="create_placeholder_on_comment_deleted"
)
def create_placeholder_on_comment_deleted(sender, instance, using, **kwargs):
    instance.create_placeholder()
