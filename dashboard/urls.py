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
    RecentNotificationsViewSet,
    UnlinkedConstituencyViewSet,
)
from dashboard.views.search import DashboardSearch


class _ListRouter(SimpleRouter):
    routes = [
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list"},
            name="{basename}-list",
            detail=False,
            initkwargs={},
        ),
    ]


class _ListOrDetailRouter(SimpleRouter):
    # Read-only list/detail views
    routes = [
        # All objects, simple overview
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list"},
            name="{basename}-list",
            detail=False,
            initkwargs={},
        ),
        # Single object, more detailed data
        Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={"get": "retrieve"},
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
    ]


list_router = _ListRouter()
list_router.register(
    "recent-notifications", RecentNotificationsViewSet, basename="recent-notifications"
)

list_or_detail_router = _ListOrDetailRouter()
list_or_detail_router.register(
    "unlinked-constituencies",
    UnlinkedConstituencyViewSet,
    basename="unlinked-constituencies",
)

urlpatterns = [
    path("", include(list_router.urls)),
    path("", include(list_or_detail_router.urls)),
    path("", DashboardView.as_view(), name="dashboard"),
    path(
        "actions/featured-person/<int:id>/",
        ToggleFeaturedMemberView.as_view(),
        name="action-featured-person",
    ),
    path(
        "actions/featured-bill/<int:id>/",
        ToggleFeaturedBillView.as_view(),
        name="action-featured-bill",
    ),
    path(
        "actions/featured-commonsdivision/<int:id>/",
        ToggleFeaturedCommonsDivisionView.as_view(),
        name="action-featured-commonsdivision",
    ),
    path(
        "actions/featured-lordsdivision/<int:id>/",
        ToggleFeaturedLordsDivisionView.as_view(),
        name="action-featured-lordsdivision",
    ),
    path("search/<str:query>/", DashboardSearch.as_view(), name="dashboard-search"),
]
