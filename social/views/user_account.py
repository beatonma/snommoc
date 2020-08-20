"""

"""
import json
import logging

from django.http import (
    HttpResponse,
)
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from social.models.token import UserToken
from social.views import contract

log = logging.getLogger(__name__)


class UserAccountView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            token = body.get(contract.USER_TOKEN)
            gtoken = body.get(contract.GOOGLE_TOKEN)
            usertoken = UserToken.objects.get(
                token=token,
                provider_account_id=gtoken,
            )
            usertoken.mark_pending_deletion()
            usertoken.save()
        except Exception as e:
            log.warning(f'Failed to delete usertoken: {e} {request.body}')
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
