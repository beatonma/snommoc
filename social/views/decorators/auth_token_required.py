"""

"""

import logging
from functools import wraps

from django.conf import settings
from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError,
)
from django.http import (
    HttpRequest,
    HttpResponse,
)

from social.models.token import UserToken

log = logging.getLogger(__name__)


class UserTokenDisabled(Exception):
    pass


def user_token_required(f):
    """
    Decorator for View.dispatch methods that require a valid auth token..
    Key must be passed as a GET param: ?key=KEY
    """
    @wraps(f)
    def verify_user_token(view, request: HttpRequest, *args, **kwargs):
        try:
            if 'token' not in request.POST:
                return HttpResponse('User token required', status=400)
            token = UserToken.objects.get(key=request.POST.get('token'))
            if token.enabled:
                log.info(f'User token verified: {token}')
                return f(view, request, *args, **kwargs)
            else:
                raise UserTokenDisabled(f'Token disabled: {token}')

        except (UserTokenDisabled, ValidationError, ObjectDoesNotExist) as e:
            log.warning(f'403: {e}')
            return HttpResponse('Invalid user token', status=403)

    return verify_user_token
