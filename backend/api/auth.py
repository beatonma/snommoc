import logging

from api import permissions
from api.models import ApiKey
from api.permissions import has_read_snommoc_api_permission
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest
from ninja.security import APIKeyQuery

log = logging.getLogger(__name__)


class ApiKeyException(Exception):
    pass


class ApiKeyDoesNotExist(ApiKeyException):
    pass


class ApiKeyDisabled(ApiKeyException):
    pass


class ApiReadAuth(APIKeyQuery):
    param_name = "key"

    def authenticate(
        self, request: HttpRequest, key: str | None
    ) -> AbstractUser | ApiKey | None:
        user = request.user
        if has_read_snommoc_api_permission(user):
            # OK
            log.info(f"User '{user}' has permission '{permissions.READ_SNOMMOC_API}'")
            return user

        try:
            api_key = ApiKey.objects.get(key=key)
            if api_key.enabled:
                # OK
                log.info(f"API key accepted for user '{api_key.user}'")
                return api_key
            else:
                raise ApiKeyDisabled()

        except ApiKey.DoesNotExist:
            raise ApiKeyDoesNotExist()
