"""

"""

import logging

from api.serializers import InlineMemberSerializer

from api.views.viewsets import KeyRequiredViewSet
from social.models import (
    RecentPersonEngagement,
)

log = logging.getLogger(__name__)


class RecentEngagementViewSet(KeyRequiredViewSet):
    def get_queryset(self):
        return [
            x.person
            for x in RecentPersonEngagement.objects.all().order_by(
                'person_id'
            )
        ]

    serializer_class = InlineMemberSerializer
