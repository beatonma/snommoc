"""

"""

import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from social.models.token import (
    UsernameChanged,
    UserToken,
)

log = logging.getLogger(__name__)


@receiver(
    pre_save,
    sender=UserToken,
    dispatch_uid='create_previous_username_on_usertoken_name_changed'
)
def create_previous_username_on_usertoken_name_changed(
        sender, instance: UserToken, *args, **kwargs
):
    try:
        existing: UserToken = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if existing.username != instance.username:
            UsernameChanged.objects.create(
                token=instance,
                new_name=instance.username,
                previous_name=existing.username,
            ).save()
