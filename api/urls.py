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
list_or_detail = ListOrDetailRouter()
list_or_detail.register(endpoints.MEMBER, MemberViewSet, basename=endpoints.MEMBER)
list_or_detail.register(endpoints.PARTY, PartyViewSet)
list_or_detail.register(endpoints.CONSTITUENCY, ConstituencyViewSet)
list_or_detail.register(endpoints.DIVISION_COMMONS, CommonsVotesViewSet)
list_or_detail.register(endpoints.FEATURED, FeaturedMembersViewSet, basename=endpoints.FEATURED)

# Views which can only return a single detailed viewset.
detail_only = DetailOnlyRouter()
detail_only.register(endpoints.ADDRESS, AddressViewSet, basename=endpoints.ADDRESS)
detail_only.register(endpoints.COMMITTEES, CommitteeViewSet, basename=endpoints.COMMITTEES)
detail_only.register(endpoints.CONSTITUENCIES, HistoricalConstituencyViewSet, basename=endpoints.CONSTITUENCIES)
detail_only.register(endpoints.CONTESTED_ELECTIONS, ContestedElectionViewSet, basename=endpoints.CONTESTED_ELECTIONS),
detail_only.register(endpoints.DECLARED_INTERESTS, DeclaredInterestViewSet, basename=endpoints.DECLARED_INTERESTS)
detail_only.register(endpoints.EXPERIENCES, ExperienceViewSet, basename=endpoints.EXPERIENCES)
detail_only.register(endpoints.MAIDEN_SPEECHES, MaidenSpeechViewSet, basename=endpoints.MAIDEN_SPEECHES)
detail_only.register(endpoints.POSTS, PostViewSet, basename=endpoints.POSTS)
detail_only.register(endpoints.PARTIES, HistoricalPartyViewSet, basename=endpoints.PARTIES)
detail_only.register(endpoints.PROFILE, ProfileViewSet, basename=endpoints.PROFILE)
detail_only.register(endpoints.SUBJECTS_OF_INTEREST, SubjectOfInterestViewSet, basename=endpoints.SUBJECTS_OF_INTEREST)


for x in list_or_detail.urls + detail_only.urls:
    print(x)

urlpatterns = [
    path('ping/', PingView.as_view(), name='api_ping_view'),
    path('', include(list_or_detail.urls)),
    path('', include(detail_only.urls)),
]
