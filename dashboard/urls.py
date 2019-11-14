from django.urls import path

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
    path('parties/', PartyDashboardView.as_view(), name='dashboard-parties'),
]
