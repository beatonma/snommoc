from django.urls import include, path
from rest_framework.routers import Route, SimpleRouter

from dashboard.views.actions import (
    ToggleFeaturedBillView,
    ToggleFeaturedCommonsDivisionView,
    ToggleFeaturedLordsDivisionView,
    ToggleFeaturedMemberView,
)
from dashboard.views.dashboard import (
    DashboardView,
    RecentNotificationsViewSet, UnlinkedConstituencyViewSet,
)
from dashboard.views.search import DashboardSearch


class _ListRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={},
        ),
    ]


router = _ListRouter()
router.register('unlinked-constituencies', UnlinkedConstituencyViewSet, basename='unlinked-constituencies')
router.register('recent-notifications', RecentNotificationsViewSet, basename='recent-notifications')

urlpatterns = [
    path('', include(router.urls)),
    path('', DashboardView.as_view(), name='dashboard'),

    path('actions/featured-person/<int:id>/',
         ToggleFeaturedMemberView.as_view(),
         name='action-featured-person'),

    path('actions/featured-bill/<int:id>/',
         ToggleFeaturedBillView.as_view(),
         name='action-featured-bill'),

    path('actions/featured-commonsdivision/<int:id>/',
         ToggleFeaturedCommonsDivisionView.as_view(),
         name='action-featured-commonsdivision'),

    path('actions/featured-lordsdivision/<int:id>/',
         ToggleFeaturedLordsDivisionView.as_view(),
         name='action-featured-lordsdivision'),

    path('search/<str:query>/',
         DashboardSearch.as_view(),
         name='dashboard-search'),
]
