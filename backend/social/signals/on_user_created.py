import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from social.models import OAuthToken
from social.models.token import UserToken

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
    oauth_session = OAuthToken.objects.create_default(instance.username)
    UserToken.objects.create(
        oauth_session=oauth_session,
        username=instance.username,
    )
