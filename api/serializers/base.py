"""

"""

import logging

from rest_framework import serializers

log = logging.getLogger(__name__)


class InlineSerializer(serializers.HyperlinkedModelSerializer):
    """Return basic data about the object with a link for further
    details if required."""
    pass


class DetailedSerializer(serializers.HyperlinkedModelSerializer):
    """Return all details about the object."""
    pass
