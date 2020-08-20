"""

"""

import logging

from django.conf import settings

log = logging.getLogger(__name__)


def get_snommoc_settings() -> dict:
    if hasattr(settings, 'SNOMMOC'):
        return settings.SNOMMOC
    return {}


def get_social_settings() -> dict:
    return get_snommoc_settings().get('SOCIAL', {})
