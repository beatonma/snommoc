import logging

from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from social.models.token import SignInServiceProvider, UserToken
from social.views import contract

log = logging.getLogger(__name__)


class VerifyGoogleTokenView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        token = request.POST.get("token", None)
        if token is None:
            log.warning("No token provided in POST data")
            return HttpResponseBadRequest("Required data is missing")

        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request())
        except Exception as e:
            log.warning(f"Token verification failed: {e}")
            return HttpResponseBadRequest("Bad token")

        audience = id_info["aud"]
        issuer = id_info["iss"]

        if audience not in settings.G_CLIENT_IDS:
            log.warning(
                f'Token has wrong audience "{audience}". Expected one of {settings.G_CLIENT_IDS}'
            )
            return HttpResponseBadRequest("Bad token")
        if issuer not in ["accounts.google.com", "https://accounts.google.com"]:
            log.warning(f"Wrong issuer: {issuer}")
            return HttpResponseBadRequest("Bad token")

        userid = id_info["sub"]

        provider, _ = SignInServiceProvider.objects.get_or_create(name="google")
        user_token, _ = UserToken.objects.get_or_create(
            provider=provider,
            provider_account_id=userid,
        )

        if user_token.pending_deletion:
            """Account is marked for deletion"""
            return JsonResponse(
                {
                    contract.USER_NAME: user_token.username,
                },
                status=status.HTTP_410_GONE,
            )

        else:
            return JsonResponse(
                {
                    contract.GOOGLE_TOKEN: token[:32],
                    contract.USER_TOKEN: user_token.token,
                    contract.USER_NAME: user_token.username,
                }
            )
