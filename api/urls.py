from django.urls import (
    path,
    include,
)

from api import endpoints as api_endpoints
from api.views.routers import SnommocRouter
from api.views.viewsets import (
    PartyViewSet,
    ConstituencyViewSet,
    MemberViewSet,
)

router = SnommocRouter()
router.register(api_endpoints.MEMBER, MemberViewSet, basename=api_endpoints.MEMBER)
router.register(api_endpoints.PARTY, PartyViewSet)
router.register(api_endpoints.CONSTITUENCY, ConstituencyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
