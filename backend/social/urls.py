from django.urls import path
from social.views.oauth_google import VerifyGoogleTokenView

from .api import api

urlpatterns = [
    path("auth/g/", VerifyGoogleTokenView.as_view(), name="gauth-verify-token"),
    path("", api.urls),
]
