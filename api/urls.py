from django.urls import (
    include,
    path,
)
from rest_framework.routers import SimpleRouter

from api import endpoints
from api.views import PingView
from api.views.viewsets.bills import BillViewSet
from api.views.viewsets.constituency import (
    ConstituencyResultDetailViewSet,
    ConstituencyViewSet,
)
from api.views.viewsets.divisions import (
    CommonsDivisionViewSet,
    LordsDivisionViewSet,
)
from api.views.viewsets.member import (
    MemberViewSet,
    MemberVotesViewSet,
    ProfileViewSet,
)
from api.views.viewsets.party import PartyViewSet
from api.views.viewsets.zeitgeist import ZeitgeistViewSet
from common.network.routers import (
    DetailOnlyRouter,
    ListOnlyRouter,
    ListOrDetailRouter,
    SingletonRouter,
)


def _register_all(router: SimpleRouter, views) -> SimpleRouter:
    for endpoint, viewset in views:
        router.register(endpoint, viewset, basename=endpoint)

    return router


"""Views which return a list of simple items."""
list_only_views = ((endpoints.MEMBER, MemberViewSet),)

"""Views which may return a list of simple items, or a single detailed item."""
list_or_detail_views = (
    (endpoints.PARTY, PartyViewSet),
    (endpoints.CONSTITUENCY, ConstituencyViewSet),
    (endpoints.DIVISION_COMMONS, CommonsDivisionViewSet),
    (endpoints.DIVISION_LORDS, LordsDivisionViewSet),
)

"""Views which can only return a single detailed view."""
detail_only_views = (
    (endpoints.BILL, BillViewSet),
    (endpoints.MEMBER_FULL_PROFILE, ProfileViewSet),
    (endpoints.MEMBER_VOTES, MemberVotesViewSet),
)

"""Detailed, but only one target object so no IDs necessary."""
singleton_views = ((endpoints.ZEITGEIST, ZeitgeistViewSet),)

routers = [
    _register_all(ListOnlyRouter(), list_only_views),
    _register_all(ListOrDetailRouter(), list_or_detail_views),
    _register_all(DetailOnlyRouter(), detail_only_views),
    _register_all(SingletonRouter(), singleton_views),
]

urlpatterns = [
    path(endpoints.PING, PingView.as_view(), name=endpoints.PING),
    path(
        endpoints.CONSTITUENCY_RESULTS,
        ConstituencyResultDetailViewSet.as_view({"get": "retrieve"}),
        name=endpoints.endpoint_name(endpoints.CONSTITUENCY_RESULTS),
    ),
] + [path("", include(router.urls)) for router in routers]
