from typing import Iterator, Type

from django.apps import apps
from django.contrib import admin
from django.db import models


def get_module_models(module_name: str) -> Iterator[Type[models.Model]]:
    repository_config = apps.get_app_config(module_name)
    return repository_config.get_models()


def register_models_to_default_admin(
    module_name: str,
    default_admin: Type[admin.ModelAdmin],
):
    """
    Any models in the module that have not already been registered will be registered with default_admin.
    """
    for model in get_module_models(module_name):
        try:
            admin.site.register(model, default_admin)
        except admin.sites.AlreadyRegistered:
            pass


class BaseAdmin(admin.ModelAdmin):
    """
    The BaseAdmin checks for common fields on the model and applies default behaviour for search, ordering
    and list display.
    """

    save_on_top = True

    default_display_fields = []

    default_ordering = [
        "name",
    ]

    default_search_fields = [
        "name",
    ]

    def __init__(self, model: Type[models.Model], admin_site):
        super().__init__(model, admin_site)

        self.list_display = self._get_default_display_fields(model)
        self.search_fields = self._get_default_search_fields(model)
        self.ordering = self._get_default_ordering(model)

    def _get_default_display_fields(self, model: Type[models.Model]) -> list[str]:
        return ["__str__"] + self._choose_fields(
            model,
            [x for x in self.list_display if x != "__str__"],
            self.default_display_fields,
        )

    def _get_default_search_fields(self, model: Type[models.Model]) -> list[str]:
        return self._choose_fields(
            model, self.search_fields, self.default_search_fields
        )

    def _get_default_ordering(self, model: Type[models.Model]) -> list[str]:
        model_ordering = list(model._meta.ordering or [])
        return self._choose_fields(
            model, model_ordering + list(self.ordering or []), self.default_ordering
        )

    def _choose_fields(self, model: Type[models.Model], existing, fields) -> list[str]:
        """
        Combine fields from the current ModelAdmin definition with the provided fields, removing any duplicates.
        """
        existing = existing or []
        fields = fields or []
        field_names = [
            (x.split("__")[0] if not x.startswith("__") else x).replace(
                "-", ""
            )  # Strip base field name from field spec: e.g. '-name' -> 'name', 'person__name' -> 'person'
            for x in fields
        ]

        # Return combination of existing and fields, excluding any that the model does not have fields for.
        result = list(
            dict.fromkeys(
                list(existing or [])
                + [x[1] for x in zip(field_names, fields) if hasattr(model, x[0])]
            )
        )
        return result
