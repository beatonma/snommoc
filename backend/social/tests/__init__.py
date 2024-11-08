from django.urls import reverse_lazy
from social.api import api


def reverse_api(view_name: str, *args, **kwargs):
    return reverse_lazy(f"{api.urls_namespace}:{view_name}", args=args, kwargs=kwargs)
