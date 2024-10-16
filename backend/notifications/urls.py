from django.urls import path

from notifications.views.notifications import (
    CreateNotificationView,
    DismissNotificationView,
    PendingNotificationsView,
    VIEW_CREATE_NOTIFICATION,
    VIEW_DISMISS_NOTIFICATION,
    VIEW_PENDING_NOTIFICATIONS,
)


urlpatterns = [
    path('pending', PendingNotificationsView.as_view(),
         name=VIEW_PENDING_NOTIFICATIONS),
    path('dismiss', DismissNotificationView.as_view(),
         name=VIEW_DISMISS_NOTIFICATION),
    path('create', CreateNotificationView.as_view(),
         name=VIEW_CREATE_NOTIFICATION),
]
