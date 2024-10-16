from django.contrib import admin

from common.admin import BaseAdmin, register_models_to_default_admin
from social.apps import SocialConfig
from social.models import Comment


class SocialAdmin(BaseAdmin):
    default_search_fields = [
        "user__username",
        "user__usertoken",
    ]

    default_display_fields = [
        "target",
        "user",
        "modified_on",
    ]

    default_ordering = [
        "modified_on",
    ]

    default_readonly_fields = BaseAdmin.default_readonly_fields + [
        "deletion_requested_at",
        "user",
        "vote_type",
        "text",
        "token",
        "previous_name",
        "new_name",
        "provider",
    ]


@admin.register(Comment)
class CommentAdmin(SocialAdmin):
    list_display = [
        "visible",
        "flagged",
        "pending_deletion",
        "text",
    ]


register_models_to_default_admin(SocialConfig.name, SocialAdmin)
