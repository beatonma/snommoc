from api import status
from crawlers.network.exceptions import HttpError
from django.conf import settings
from django.http import HttpRequest
from google.auth.transport import requests
from google.oauth2 import id_token
from ninja import Router
from social.models import OAuthToken, UserToken

from . import schema

router = Router(tags=["Auth"])


@router.post("/g/", response=schema.UserLoginResponse)
def verify_google_token(request: HttpRequest, data: schema.GoogleAuthRequest):
    response = schema.JsonWebToken.model_validate(
        id_token.verify_oauth2_token(
            data.encoded_oauth_token,
            requests.Request(),
            audience=settings.G_CLIENT_ID,
        )
    )

    oauth_session, _ = OAuthToken.objects.update_or_create(
        provider="google",
        user_id=response.user_id,
    )

    user_token, _ = UserToken.objects.get_or_create(
        oauth_session=oauth_session,
    )

    if user_token.pending_deletion:
        raise HttpError(status.HTTP_410_GONE, {"username": user_token.username})

    return {
        "token": user_token.token.hex,
        "username": user_token.username,
    }
