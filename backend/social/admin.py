from common.admin import BaseAdmin, register_models_to_default_admin
from django.contrib import admin
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
        "modified_at",
    ]

    default_ordering = [
        "modified_at",
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
