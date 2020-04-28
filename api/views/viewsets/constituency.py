"""

"""

import logging

from api.serializers import (
    ConstituencySerializer,
    InlineConstituencySerializer,
)
from api.serializers.constituencies import ElectionResultSerializer
from api.views.viewsets import (
    KeyRequiredViewSet,
    Searchable,
)
from repository.models import (
    Constituency,
    ConstituencyResult,
)

log = logging.getLogger(__name__)


class ConstituencyViewSet(Searchable, KeyRequiredViewSet):
    """Parliamentary constituency."""
    queryset = Constituency.objects.all()
    search_fields = [
        'name'
    ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConstituencySerializer
        else:
            return InlineConstituencySerializer
