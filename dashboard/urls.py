from django.urls import path

from dashboard.views.actions import (
    AddFeaturedBillView,
    AddFeaturedMemberView,
)
from dashboard.views.dashboard import (
    DashboardView,
)
from dashboard.views.profile import MemberProfileView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('actions/add-featured-person/',
         AddFeaturedMemberView.as_view(),
         name='action-add-featured-person'),

    path('actions/add-featured-bill/',
         AddFeaturedBillView.as_view(),
         name='action-add-featured-bill'),

    path('profile/<int:pk>/',
         MemberProfileView.as_view(),
         name='dashboard-member-profile'),
]
