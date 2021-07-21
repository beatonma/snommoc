from django.urls import (
    path,
    include,
)

from api import endpoints
from api.views import PingView
from api.views.viewsets.constituency import (
    ConstituencyResultDetailViewSet,
    ConstituencyViewSet,
)
from api.views.viewsets.divisions import (
    CommonsDivisionViewSet,
    RecentlyUpdatedDivisionsViewSet,
    LordsDivisionViewSet,
)
from api.views.viewsets.member import (
    MemberViewSet,
    FeaturedMembersViewSet,
    MemberVotesViewSet,
    ProfileViewSet,
    MemberCommonsVotesViewSet,
    MemberLordsVotesViewSet,
)
from api.views.viewsets.party import PartyViewSet
from api.views.viewsets.bills import (
    BillViewSet,
    RecentlyUpdatedBillsViewSet,
)
from api.views.viewsets.zeitgeist import ZeitgeistViewSet
from common.network.routers import (
    DetailOnlyRouter,
    ListOnlyRouter,
    ListOrDetailRouter,
    SingletonRouter,
)


def _register(router, endpoint, viewset):
    router.register(endpoint, viewset, basename=endpoint)


list_only_views = (
    (endpoints.FEATURED_MEMBERS, FeaturedMembersViewSet),
    (endpoints.FEATURED_BILLS, RecentlyUpdatedBillsViewSet),
    (endpoints.FEATURED_DIVISIONS, RecentlyUpdatedDivisionsViewSet),
)

# Views which may return an overview of a list or detail for a single item
list_or_detail_views = (
    (endpoints.MEMBER, MemberViewSet),
    (endpoints.PARTY, PartyViewSet),
    (endpoints.CONSTITUENCY, ConstituencyViewSet),
    (endpoints.DIVISION_COMMONS, CommonsDivisionViewSet),
    (endpoints.DIVISION_LORDS, LordsDivisionViewSet),
)

# Views which can only return a single detailed viewset.
detail_only_views = (
    (endpoints.BILL, BillViewSet),
    (endpoints.MEMBER_FULL_PROFILE, ProfileViewSet),
    (endpoints.MEMBER_VOTES, MemberVotesViewSet),
    (endpoints.MEMBER_VOTES_COMMONS, MemberCommonsVotesViewSet),
    (endpoints.MEMBER_VOTES_LORDS, MemberLordsVotesViewSet),
)

# Detailed, but only one target object so no IDs necessary.
singleton_views = ((endpoints.ZEITGEIST, ZeitgeistViewSet),)

list_only_router = ListOnlyRouter()
for e, v in list_only_views:
    _register(list_only_router, e, v)

list_or_detail_router = ListOrDetailRouter()
for e, v in list_or_detail_views:
    _register(list_or_detail_router, e, v)

detail_only_router = DetailOnlyRouter()
for e, v in detail_only_views:
    _register(detail_only_router, e, v)

singleton_router = SingletonRouter()
for e, v in singleton_views:
    _register(singleton_router, e, v)

urlpatterns = [
    path("ping/", PingView.as_view(), name="api_ping_view"),
    path("", include(list_only_router.urls)),
    path("", include(list_or_detail_router.urls)),
    path("", include(detail_only_router.urls)),
    path("", include(singleton_router.urls)),
    # This one requires 2 keys
    path(
        f"{endpoints.CONSTITUENCY}/<int:pk>/election/<int:election_id>/",
        ConstituencyResultDetailViewSet.as_view({"get": "retrieve"}),
        name=endpoints.CONSTITUENCY_RESULTS,
    ),
]
