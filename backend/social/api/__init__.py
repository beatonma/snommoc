from api import status
from django.http import HttpRequest
from ninja import NinjaAPI

from .interactions import router as interactions_router

__version__ = "2.0"

from .errors import BadUserToken

api = NinjaAPI(urls_namespace=f"social_api-{__version__}", version=__version__)

api.add_router("", interactions_router)


@api.exception_handler(BadUserToken)
def missing_usertoken(request: HttpRequest, exception: Exception):
    return api.create_response(
        request,
        {"message": "Bad token"},
        status=status.HTTP_403_FORBIDDEN,
    )
