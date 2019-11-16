from django.urls import path

from dashboard.views.actions import (
    UpdateConstituenciesView,
    UpdateMpsView,
)
from dashboard.views.dashboard import (
    ConstituencyDashboardView,
    DashboardView,
    MpDashboardView,
    PartyDashboardView,
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('mps/', MpDashboardView.as_view(), name='dashboard-mps'),
    path('mps/<str:requirement>/', MpDashboardView.as_view(), name='dashboard-mps'),
    path('constituencies/', ConstituencyDashboardView.as_view(), name='dashboard-constituencies'),
    path('constituencies/<str:requirement>/', ConstituencyDashboardView.as_view(), name='dashboard-constituencies'),
    path('parties/', PartyDashboardView.as_view(), name='dashboard-parties'),
    path('parties/<str:requirement>/', PartyDashboardView.as_view(), name='dashboard-parties'),

    path('actions/update-constituencies/', UpdateConstituenciesView.as_view(), name='action-update-constituencies'),
    path('actions/update-constituencies/<str:requirement>/', UpdateConstituenciesView.as_view(), name='action-update-constituencies'),
    path('actions/update-mps/', UpdateMpsView.as_view(), name='action-update-mps'),
    path('actions/update-mps/<str:requirement>/', UpdateMpsView.as_view(), name='action-update-mps'),
]
