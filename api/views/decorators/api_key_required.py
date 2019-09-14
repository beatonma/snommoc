from functools import wraps
import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpRequest, HttpResponse

from api import contract
from api.models import ApiKey

log = logging.getLogger(__name__)


class ApiKeyDisabled(Exception):
    pass


def api_key_required(f):
    """
    Decorator for View.dispatch methods that require a valid API key.
    Key must be passed as a GET param: ?key=KEY
    """
    @wraps(f)
    def verify_api_key(view, request: HttpRequest, *args, **kwargs):
        if settings.DEBUG:
            return f(view, request, *args, user=request.user, **kwargs)

        try:
            if 'key' not in request.GET:
                return HttpResponse('API key required', status=400)
            key = ApiKey.objects.get(key=request.GET.get(contract.API_KEY))
            if key.enabled:
                log.debug(f'API Key verified for User=\'{key.user}\'')
                return f(view, request, *args, user=key.user, **kwargs)
            else:
                raise ApiKeyDisabled(f'Key disabled for User=\'{key.user}\'')

        except (ApiKeyDisabled, ValidationError, ObjectDoesNotExist) as e:
            log.warning(f'403: {e}')
            return HttpResponse('Invalid API key', status=403)

    return verify_api_key
