"""

"""

import logging

from django.conf import settings
from django.http import (
    HttpResponseBadRequest,
    JsonResponse,
)
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from google.auth.transport import requests
from google.oauth2 import id_token

from api.views.decorators import api_key_required
from social.models.token import (
    SignInServiceProvider,
    UserToken,
)

log = logging.getLogger(__name__)


class VerifyGoogleTokenView(View):
    @csrf_exempt
    @api_key_required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        token = request.POST.get('token', None)
        if token is None:
            log.warning('No token provided in POST data')
            return HttpResponseBadRequest()

        id_info = id_token.verify_oauth2_token(token, requests.Request())
        audience = id_info['aud']
        issuer = id_info['iss']

        if audience not in settings.G_CLIENT_IDS:
            log.warning(f'Token has wrong audience "{audience}". Expected one of {settings.G_CLIENT_IDS}')
            return HttpResponseBadRequest()
        if issuer not in ['accounts.google.com', 'https://accounts.google.com']:
            log.warning(f'Wrong issuer: {issuer}')
            return HttpResponseBadRequest()

        userid = id_info['sub']

        provider, _ = SignInServiceProvider.objects.get_or_create(name='google')
        g_user_token, _ = UserToken.objects.get_or_create(
            provider=provider,
            account_id=userid,
        )
        return JsonResponse({
            'token': g_user_token.token,
        })
