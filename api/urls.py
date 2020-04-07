from django.urls import (
    path,
    include,
)

from api import endpoints
from api.views.routers import (
    DetailOnlyRouter,
    ListOrDetailRouter,
    ListOnlyRouter,
)
from api.views.viewsets.member import (
    PartyViewSet,
    ConstituencyViewSet,
    MemberViewSet,
    FeaturedMembersViewSet,
    MemberVotesViewSet,
    ProfileViewSet,
    MemberCommonsVotesViewSet,
    MemberLordsVotesViewSet,
)
from api.views.views import PingView

# Views which can return a list of inline viewsets, or a single detailed viewset.
from api.views.viewsets.procedure import (
    FeaturedBillsViewSet,
    BillViewSet,
    CommonsDivisionViewSet,
    LordsDivisionViewSet,
)


def _register(router, endpoint, viewset):
    router.register(endpoint, viewset, basename=endpoint)


list_only_views = (
    (endpoints.FEATURED_MEMBERS, FeaturedMembersViewSet),
    (endpoints.FEATURED_BILLS, FeaturedBillsViewSet),
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

list_only_router = ListOnlyRouter()
for e, v in list_only_views:
    _register(list_only_router, e, v)

list_or_detail_router = ListOrDetailRouter()
for e, v in list_or_detail_views:
    _register(list_or_detail_router, e, v)

detail_only_router = DetailOnlyRouter()
for e, v in detail_only_views:
    _register(detail_only_router, e, v)


for x in list_only_router.urls + list_or_detail_router.urls + detail_only_router.urls:
    print(x)

urlpatterns = [
    path('ping/', PingView.as_view(), name='api_ping_view'),
    path('', include(list_only_router.urls)),
    path('', include(list_or_detail_router.urls)),
    path('', include(detail_only_router.urls)),
]
