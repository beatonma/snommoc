"""

"""

import logging

from django.urls import (
    include,
    path,
)

from social.views.oauth_google import VerifyGoogleTokenView
from social.views.routers import SocialRouter
from social.views.viewsets.social import MemberSocialViewSet

log = logging.getLogger(__name__)

social_router = SocialRouter()
social_router.register('member', MemberSocialViewSet, 'social-member')


urlpatterns = [
    path('auth/g/', VerifyGoogleTokenView.as_view(), name='gauth-verify-token'),
    path('', include(social_router.urls)),
]
