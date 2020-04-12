"""

"""

import logging

from django.contrib import admin

from social.models.token import UserToken

log = logging.getLogger(__name__)


@admin.register(
    UserToken
)
class DefaultSocialAdmin(admin.ModelAdmin):
    pass
