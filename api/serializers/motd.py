"""

"""

import logging

from api.serializers import DetailedModelSerializer
from surface.models import MessageOfTheDay

log = logging.getLogger(__name__)


class MessageOfTheDaySerializer(DetailedModelSerializer):

    class Meta:
        model = MessageOfTheDay
        fields = [
            'title',
            'description',
            'action_url',
        ]
