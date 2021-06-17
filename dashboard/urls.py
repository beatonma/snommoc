from django.urls import include, path, re_path

from common.network.routers import ListOnlyRouter, ListOrDetailRouter
from dashboard.views.actions import (
    ConfirmConstituencyView,
    ToggleFeaturedBillView,
    ToggleFeaturedCommonsDivisionView,
    ToggleFeaturedLordsDivisionView,
    ToggleFeaturedMemberView,
    UpdateBillsTaskView,
    UpdateDivisionsTaskView,
    UpdateElectionResultsTaskView,
    UpdatePortraitsTaskView,
    UpdateProfilesTaskView,
)
from dashboard.views.active_members import ActiveMembersView
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
    path("search/<str:query>/", DashboardSearch.as_view(), name="dashboard-search"),
    path(
        "actions/featured-person/<int:id>/",
        ToggleFeaturedMemberView.as_view(),
        name="dashboard-action-featured-person",
    ),
    path(
        "actions/featured-bill/<int:id>/",
        ToggleFeaturedBillView.as_view(),
        name="dashboard-action-featured-bill",
    ),
    path(
        "actions/featured-commonsdivision/<int:id>/",
        ToggleFeaturedCommonsDivisionView.as_view(),
        name="dashboard-action-featured-commonsdivision",
    ),
    path(
        "actions/featured-lordsdivision/<int:id>/",
        ToggleFeaturedLordsDivisionView.as_view(),
        name="dashboard-action-featured-lordsdivision",
    ),
    path(
        "actions/confirm-constituency/<int:unlinked_id>/<int:constituency_id>/",
        ConfirmConstituencyView.as_view(),
        name="dashboard-action-confirm-constituency",
    ),
    path(
        "actions/update-profiles/",
        UpdateProfilesTaskView.as_view(),
        name="dashboard-action-update-profiles",
    ),
    path(
        "actions/update-portraits/",
        UpdatePortraitsTaskView.as_view(),
        name="dashboard-action-update-portraits",
    ),
    path(
        "actions/update-bills/",
        UpdateBillsTaskView.as_view(),
        name="dashboard-action-update-bills",
    ),
    path(
        "actions/update-divisions/",
        UpdateDivisionsTaskView.as_view(),
        name="dashboard-action-update-divisions",
    ),
    path(
        "actions/update-election-results/",
        UpdateElectionResultsTaskView.as_view(),
        name="dashboard-action-update-election-results",
    ),
    path(
        "active-members/",
        ActiveMembersView.as_view(),
        name="dashboard-active-members",
    ),
    re_path(".*", DashboardView.as_view(), name="dashboard"),
]
