from django.urls import (
    path,
    include,
)

from api import endpoints
from api.views.routers import (
    DetailOnlyRouter,
    ListOrDetailRouter,
)
from api.views.viewsets.member import (
    PartyViewSet,
    ConstituencyViewSet,
    MemberViewSet,
    AddressViewSet,
    PostViewSet,
    DeclaredInterestViewSet,
    CommitteeViewSet,
    ProfileViewSet,
    ExperienceViewSet,
    ContestedElectionViewSet,
    HistoricalConstituencyViewSet,
    HistoricalPartyViewSet,
    MaidenSpeechViewSet,
    SubjectOfInterestViewSet,
    CommonsVotesViewSet,
    FeaturedMembersViewSet,
)
from api.views.views import PingView

# Views which can return a list of inline viewsets, or a single detailed viewset.
from api.views.viewsets.procedure import (
    FeaturedBillsViewSet,
    BillViewSet,
)


def _register(router, endpoint, viewset):
    router.register(endpoint, viewset, basename=endpoint)


# Views which may return an overview of a list or detail for a single item
list_or_detail_views = (
    (endpoints.MEMBER, MemberViewSet),
    (endpoints.PARTY, PartyViewSet),
    (endpoints.CONSTITUENCY, ConstituencyViewSet),
    (endpoints.DIVISION_COMMONS, CommonsVotesViewSet),
    (endpoints.FEATURED_MEMBERS, FeaturedMembersViewSet),
    (endpoints.FEATURED_BILLS, FeaturedBillsViewSet),
)

# Views which can only return a single detailed viewset.
detail_only_views = (
    (endpoints.ADDRESS, AddressViewSet),
    (endpoints.COMMITTEES, CommitteeViewSet),
    (endpoints.CONSTITUENCIES, HistoricalConstituencyViewSet),
    (endpoints.CONTESTED_ELECTIONS, ContestedElectionViewSet),
    (endpoints.DECLARED_INTERESTS, DeclaredInterestViewSet),
    (endpoints.EXPERIENCES, ExperienceViewSet),
    (endpoints.MAIDEN_SPEECHES, MaidenSpeechViewSet),
    (endpoints.POSTS, PostViewSet),
    (endpoints.PARTIES, HistoricalPartyViewSet),
    (endpoints.PROFILE, ProfileViewSet),
    (endpoints.SUBJECTS_OF_INTEREST, SubjectOfInterestViewSet),
    (endpoints.BILL, BillViewSet),
)


list_or_detail = ListOrDetailRouter()
for e, v in list_or_detail_views:
    _register(list_or_detail, e, v)

detail_only = DetailOnlyRouter()
for e, v in detail_only_views:
    _register(detail_only, e, v)


for x in list_or_detail.urls + detail_only.urls:
    print(x)

urlpatterns = [
    path('ping/', PingView.as_view(), name='api_ping_view'),
    path('', include(list_or_detail.urls)),
    path('', include(detail_only.urls)),
]
