"""

"""

import logging

from django.urls import path

from social.views.oauth_google import VerifyGoogleTokenView

log = logging.getLogger(__name__)

urlpatterns = [
    path('g/', VerifyGoogleTokenView.as_view(), name='gauth-verify-token'),
]
