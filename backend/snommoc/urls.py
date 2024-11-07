"""snommoc URL Configuration"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("api/notifications/", include("notifications.urls")),
    path("api/social/", include("social.urls")),
    path("api/", include("api.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.DASHBOARD_URL, include("dashboard.urls")),
    path("", RedirectView.as_view(url="/about")),
] + debug_toolbar_urls()
