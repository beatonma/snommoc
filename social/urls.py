"""

"""

import logging

from django.urls import (
    include,
    path,
)

from social.views.oauth_google import VerifyGoogleTokenView
from social.views.routers import SocialRouter
from social.views.user_account import UserAccountView
from social.views.viewsets.social import (
    BillSocialViewSet,
    CommonsDivisionSocialViewSet,
    LordsDivisionSocialViewSet,
    MemberSocialViewSet, ConstituencySocialViewSet, ConstituencyResultSocialViewSet,
)

log = logging.getLogger(__name__)

social_router = SocialRouter()
social_router.register('member', MemberSocialViewSet, 'social-member')
social_router.register('bill', BillSocialViewSet, 'social-bill')
social_router.register('division_commons', CommonsDivisionSocialViewSet, 'social-division-commons')
social_router.register('division_lords', LordsDivisionSocialViewSet, 'social-division-lords')
social_router.register('constituency', ConstituencySocialViewSet, 'social-constituency')
social_router.register('constituency_result', ConstituencyResultSocialViewSet, 'social-constituency-result')


urlpatterns = [
    path('account/', UserAccountView.as_view(), name='social-account-view'),
    path('auth/g/', VerifyGoogleTokenView.as_view(), name='gauth-verify-token'),
    path('', include(social_router.urls)),
]
