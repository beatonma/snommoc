from django.urls import (
    path,
    include,
)

from api import endpoints as api_endpoints
from api.views.routers import SnommocRouter
from api.views.viewsets import (
    PartyViewSet,
    ConstituencyViewSet,
    MpViewSet,
)

router = SnommocRouter()
router.register(api_endpoints.MP, MpViewSet)
router.register(api_endpoints.PARTY, PartyViewSet)
router.register(api_endpoints.CONSTITUENCY, ConstituencyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
