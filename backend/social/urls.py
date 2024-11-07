from django.urls import path
from social.views.oauth_google import VerifyGoogleTokenView
from social.views.user_account import UserAccountView

from .api import api

urlpatterns = [
    path("account/", UserAccountView.as_view(), name="social-account-view"),
    path("auth/g/", VerifyGoogleTokenView.as_view(), name="gauth-verify-token"),
    path("", api.urls),
]
