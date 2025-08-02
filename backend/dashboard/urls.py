from django.urls import path, re_path

from dashboard.api import api
from dashboard.views.active_members import ActiveMembersView
from dashboard.views.dashboard import DashboardView
from dashboard.views.search import DashboardSearch

urlpatterns = [
    path("api/", api.urls),
    path("search/<str:query>/", DashboardSearch.as_view(), name="dashboard-search"),
    path(
        "active-members/",
        ActiveMembersView.as_view(),
        name="dashboard-active-members",
    ),
    re_path(".*", DashboardView.as_view(), name="dashboard-webapp"),
]
