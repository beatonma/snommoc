from api import status
from api.auth import ApiKeyDisabled, ApiKeyDoesNotExist, ApiKeyException, ApiReadAuth
from api.routers import (
    bills_router,
    constituency_router,
    division_router,
    election_router,
    members_router,
    party_router,
    zeitgeist_router,
)
from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI
from ninja.constants import NOT_SET
from util.settings import snommoc_settings

ninja_api = NinjaAPI(
    title="snommoc",
    version="2.0",
    docs_url="/docs/",
    auth=ApiReadAuth() if snommoc_settings.auth.api_read_requires_auth else NOT_SET,
)
ninja_api.add_router("/members/", members_router)
ninja_api.add_router("/bills/", bills_router)
ninja_api.add_router("/constituencies/", constituency_router)
ninja_api.add_router("/divisions/", division_router)
ninja_api.add_router("/elections/", election_router)
ninja_api.add_router("/parties/", party_router)
ninja_api.add_router("/zeitgeist/", zeitgeist_router)


@ninja_api.get("/ping/")
def ping(request: HttpRequest):
    return ninja_api.create_response(request, "OK", status=status.HTTP_200_OK)


@ninja_api.exception_handler(ApiKeyDisabled)
def disabled_api_key(request: HttpRequest, exception: Exception):
    return ninja_api.create_response(
        request,
        {"message": "API key is not enabled."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@ninja_api.exception_handler(ApiKeyDoesNotExist)
def bad_api_key(request: HttpRequest, exception: Exception):
    return ninja_api.create_response(
        request,
        {"message": "Bad API key."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


urlpatterns = [
    path("", ninja_api.urls),
]
