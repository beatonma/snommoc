from api import status
from api.auth import ApiKeyDisabled, ApiKeyDoesNotExist, ApiKeyInvalid, ApiReadAuth
from api.routers import (
    bills_router,
    constituency_router,
    division_router,
    election_router,
    maps_router,
    members_router,
    organisations_router,
    party_router,
    zeitgeist_router,
)
from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI, Router
from ninja.constants import NOT_SET
from util.settings import snommoc_settings

ninja_api = NinjaAPI(
    title="snommoc",
    version="2.0",
    docs_url="/docs/",
)

# No auth on root API so we can allow /ping/ to be always accessible.
# All data routers go through proxy_router to respect auth settings.
proxy_router = Router(
    auth=ApiReadAuth() if snommoc_settings.auth.api_read_requires_auth else NOT_SET,
)
proxy_router.add_router("bills/", bills_router)
proxy_router.add_router("constituencies/", constituency_router)
proxy_router.add_router("divisions/", division_router)
proxy_router.add_router("elections/", election_router)
proxy_router.add_router("maps/", maps_router)
proxy_router.add_router("members/", members_router)
proxy_router.add_router("organisations/", organisations_router)
proxy_router.add_router("parties/", party_router)
proxy_router.add_router("zeitgeist/", zeitgeist_router)

ninja_api.add_router("", proxy_router)


@ninja_api.get("/ping/")
def ping(request: HttpRequest):
    return ninja_api.create_response(request, "OK", status=status.HTTP_200_OK)


@ninja_api.api_operation(["HEAD"], "/ping/", response={204: None})
def ping(request: HttpRequest):
    return 204, None


@ninja_api.exception_handler(ApiKeyDisabled)
def disabled_api_key(request: HttpRequest, exception: Exception):
    return ninja_api.create_response(
        request,
        {"message": "API key is not enabled."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@ninja_api.exception_handler(ApiKeyDoesNotExist)
@ninja_api.exception_handler(ApiKeyInvalid)
def bad_api_key(request: HttpRequest, exception: Exception):
    return ninja_api.create_response(
        request,
        {"message": "Bad API key."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


urlpatterns = [
    path("", ninja_api.urls),
]
