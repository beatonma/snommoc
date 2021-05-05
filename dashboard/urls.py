from django.urls import include, path

from common.network.routers import ListOnlyRouter, ListOrDetailRouter
from dashboard.views.actions import (
    ConfirmConstituencyView,
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


list_router = ListOnlyRouter()
list_router.register(
    "recent-notifications", RecentNotificationsViewSet, basename="recent-notifications"
)

list_or_detail_router = ListOrDetailRouter()
list_or_detail_router.register(
    "unlinked-constituencies",
    UnlinkedConstituencyViewSet,
    basename="unlinked-constituencies",
)

urlpatterns = [
    path("", include(list_router.urls)),
    path("", include(list_or_detail_router.urls)),
    path("", DashboardView.as_view(), name="dashboard"),
    path("search/<str:query>/", DashboardSearch.as_view(), name="dashboard-search"),
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
    path(
        "actions/confirm-constituency/<int:unlinked_id>/<int:constituency_id>/",
        ConfirmConstituencyView.as_view(),
        name="action-confirm-constituency",
    ),
]
