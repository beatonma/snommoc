"""snommoc URL Configuration"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    [
        path("api/notifications/", include("notifications.urls")),
        # path("api/social/", include("social.urls")),   # Disabled for public demo
        path("api/", include("api.urls")),
        path(settings.ADMIN_URL, admin.site.urls),
    ]
    + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
