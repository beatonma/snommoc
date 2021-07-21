import logging

from django.conf import settings
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from social.models.token import (
    SignInServiceProvider,
    UserToken,
)

log = logging.getLogger(__name__)


@receiver(
    post_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="create_usertoken_on_user_created",
)
def create_usertoken_on_user_created(sender, instance, created, **kwargs):
    if created:
        _create_usertoken_for_user(instance)


def _create_usertoken_for_user(instance):
    signin_provider, _ = SignInServiceProvider.objects.get_or_create(name="snommoc.org")
    try:
        UserToken.objects.create(
            provider=signin_provider,
            provider_account_id=instance.username,
            username=instance.username,
        )
    except IntegrityError as e:
        log.warning(f"Unable to create UserToken for new user: {e}")
