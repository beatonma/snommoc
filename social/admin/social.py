"""

"""

import logging

from django.contrib import admin

from social.models import (
    Comment,
    Vote,
    VoteType,
)
from social.models.token import UserToken, UsernameChanged

log = logging.getLogger(__name__)


@admin.register(
    UserToken,
    VoteType,
    UsernameChanged,
)
class DefaultSocialAdmin(admin.ModelAdmin):
    save_on_top = True
    pass


@admin.register(
    Comment,
)
class CommentAdmin(DefaultSocialAdmin):
    list_display = [
        'user',
        'flagged',
        'modified_on',
        'visible',
        'text',
    ]
    ordering = [
        'modified_on',
        'user',
    ]


@admin.register(
    Vote,
)
class VoteAdmin(DefaultSocialAdmin):
    list_display = [
        'user',
        'target',
        'vote_type',
    ]
