from api import status
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from ninja import NinjaAPI

from .account import router as account_router
from .auth import router as auth_router
from .interactions import router as interactions_router

__version__ = "2.0"

from social.validation.username import BlockedUsername

from .errors import BadUserToken

api = NinjaAPI(urls_namespace=f"social_api-{__version__}", version=__version__)

api.add_router("auth/", auth_router)
api.add_router("account/", account_router)
api.add_router("", interactions_router)


@api.exception_handler(BadUserToken)
def missing_usertoken(request: HttpRequest, exception: Exception):
    return api.create_response(
        request,
        {"message": "Bad token"},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api.exception_handler(BlockedUsername)
def blocked_username(request: HttpRequest, exception: Exception):
    return api.create_response(
        request,
        {"message": "Username not allowed"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api.exception_handler(ValidationError)
def invalid_data(request: HttpRequest, exception: Exception):
    return api.create_response(
        request,
        {"message": "Invalid data"},
        status=status.HTTP_400_BAD_REQUEST,
    )
