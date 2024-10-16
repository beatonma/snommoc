from common.admin import BaseAdmin, register_models_to_default_admin
from surface.apps import SurfaceConfig


class SurfaceAdmin(BaseAdmin):
    default_display_fields = ["display", "reason", "start", "end"]

    default_ordering = ["-start", "-priority"]

    default_search_fields = [
        "title",
    ]


register_models_to_default_admin(SurfaceConfig.name, SurfaceAdmin)
