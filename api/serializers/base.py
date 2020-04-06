"""

"""

import logging

from rest_framework import serializers

log = logging.getLogger(__name__)


class InlineModelSerializer(serializers.HyperlinkedModelSerializer):
    """Return basic data about the object with a link for further
    details if required."""
    pass


class DetailedModelSerializer(serializers.HyperlinkedModelSerializer):
    """Return all details about the object."""
    pass
