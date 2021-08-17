from django.conf import settings


def get_snommoc_settings() -> dict:
    if hasattr(settings, "SNOMMOC"):
        return settings.SNOMMOC
    return {}


def get_social_settings() -> dict:
    return get_snommoc_settings().get("SOCIAL", {})


def get_cache_settings() -> dict:
    return get_snommoc_settings().get("CACHE", {})
