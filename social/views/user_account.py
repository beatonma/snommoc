"""

"""
import json
import logging

from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from api.views.decorators import api_key_required
from social.models.token import UserToken
from social.validation.username import (
    BlockedUsername,
    is_username_blocked,
)
from social.views import contract

log = logging.getLogger(__name__)


class UserAccountView(View):
    @api_key_required
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Return the username associated with the given token."""
        try:
            params = request.GET
            token = params.get(contract.USER_TOKEN)

            if not token:
                raise Exception('Missing required token')

            user_token = UserToken.objects.get(token=token)

            return JsonResponse(
                {
                    contract.USER_NAME: user_token.username,
                },
                status=status.HTTP_200_OK
            )

        except UserToken.DoesNotExist as e:
            log.warning(f'No account found for received token: {e}')
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            log.warning(f'Failed to retrieve username: {e}')
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            action = body.get(contract.ACCOUNT_ACTION)
            if not action:
                raise Exception('Missing required action')

            if action == contract.ACCOUNT_CHANGE_USERNAME:
                return self._rename_account(body)

        except Exception as e:
            log.warning(e)

        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            token = body.get(contract.USER_TOKEN)
            gtoken = body.get(contract.GOOGLE_TOKEN)

            if not token or not gtoken:
                raise Exception('Missing required token(s)')

            usertoken = UserToken.objects.get(
                token=token,
                provider_account_id=gtoken,
            )
            usertoken.mark_pending_deletion()
            usertoken.save()
            log.info(f'Account marked for deletion: {token}')

        except json.JSONDecodeError as e:
            log.warning(f'Failed to delete usertoken: {e}')
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        except UserToken.DoesNotExist as e:
            log.warning(f'No account found for received tokens: {e}')
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            log.warning(f'Failed to delete usertoken: {e}')
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        return HttpResponse(status=status.HTTP_202_ACCEPTED)

    def _rename_account(self, body) -> HttpResponse:
        try:
            token = body.get(contract.USER_TOKEN)

            if not token:
                raise Exception('Missing required token')

            existing_username = body.get(contract.USER_NAME)
            new_username = body.get(contract.ACCOUNT_NEW_USERNAME)

            if is_username_blocked(new_username):
                raise BlockedUsername(new_username)

            usertoken = UserToken.objects.get(
                token=token,
                username=existing_username
            )
            usertoken.username = new_username
            usertoken.full_clean()
            usertoken.save()
            log.info(f'Account renamed: {existing_username} -> {new_username}')

        except json.JSONDecodeError as e:
            log.warning(f'Failed to change username: {e}')
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        except UserToken.DoesNotExist as e:
            log.warning(f'Cannot find account to rename: {e}')
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        except (BlockedUsername, ValidationError) as e:
            log.warning(f'Prevented user rename: {e}')
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            log.warning(f'Failed to rename account: {e}')
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
