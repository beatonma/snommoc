from django.urls import path

from dashboard.views.actions import (
    UpdateConstituenciesView,
    UpdateMpsView,
    UpdatePartiesView,
    RebuildAllView,
)
from dashboard.views.dashboard import (
    ConstituencyDashboardView,
    DashboardView,
    MpDashboardView,
    PartyDashboardView,
    MemberDashboardView,
    LordDashboardView,
)
from dashboard.views.profile import MemberProfileView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('members/', MemberDashboardView.as_view(), name='dashboard-members'),
    path('members/<str:requirement>/', MemberDashboardView.as_view(), name='dashboard-members'),
    path('mps/', MpDashboardView.as_view(), name='dashboard-mps'),
    path('mps/<str:requirement>/', MpDashboardView.as_view(), name='dashboard-mps'),
    path('lords/', LordDashboardView.as_view(), name='dashboard-lords'),
    path('lords/<str:requirement>/', LordDashboardView.as_view(), name='dashboard-lords'),
    path('constituencies/', ConstituencyDashboardView.as_view(), name='dashboard-constituencies'),
    path('constituencies/<str:requirement>/', ConstituencyDashboardView.as_view(), name='dashboard-constituencies'),
    path('parties/', PartyDashboardView.as_view(), name='dashboard-parties'),
    path('parties/<str:requirement>/', PartyDashboardView.as_view(), name='dashboard-parties'),

    path('actions/update-constituencies/', UpdateConstituenciesView.as_view(), name='action-update-constituencies'),
    path('actions/update-constituencies/<str:requirement>/', UpdateConstituenciesView.as_view(), name='action-update-constituencies'),

    path('actions/update-mps/', UpdateMpsView.as_view(), name='action-update-mps'),
    path('actions/update-mps/<str:requirement>/', UpdateMpsView.as_view(), name='action-update-mps'),

    path('actions/update-parties/', UpdatePartiesView.as_view(), name='action-update-parties'),
    path('actions/update-parties/<str:requirement>/', UpdatePartiesView.as_view(), name='action-update-parties'),

    path('actions/rebuild/', RebuildAllView.as_view(), name='action-rebuild-all'),

    path('profile/<int:parliamentdotuk>/', MemberProfileView.as_view(), name='member-profile'),
]
