import logging
from typing import Type

from django.http import HttpRequest
from ninja import Router
from surface.models import (
    FeaturedBill,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
    FeaturedPerson,
)
from surface.models.featured import BaseFeatured
from surface.tasks import update_zeitgeist
from util.time import get_today

log = logging.getLogger(__name__)
router = Router(tags=["Zeitgeist: featured items"])


def register_model(model: Type[BaseFeatured], label: str):
    """Dynamically create `post` and `delete` endpoints for each model.

    post label/target_id/: Create a featured item
    delete label/target_id/: Remove a featured item

    Function names are set dynamically.to ensure unique `operationid` for OpenAPI"""

    def post_func(request: HttpRequest, target_id: int):
        model.objects.update_or_create(
            target_id=target_id, defaults={"start": get_today()}
        )
        update_zeitgeist()
        return 204, None

    def delete_func(request: HttpRequest, target_id: int):
        model.objects.get(target_id=target_id).delete()
        update_zeitgeist()
        return 204, None

    post_func.__name__ = f"post_{label}"
    delete_func.__name__ = f"delete_{label}"

    router.post(
        f"{label}/{{target_id}}/",
        response={204: None},
        summary=f"Create {model_class.__name__}",
    )(post_func)

    router.delete(
        f"{label}/{{target_id}}/",
        response={204: None},
        summary=f"Delete {model_class.__name__}",
    )(delete_func)


for model_class, urlpath_label in [
    (FeaturedPerson, "person"),
    (FeaturedBill, "bill"),
    (FeaturedCommonsDivision, "commons-division"),
    (FeaturedLordsDivision, "lords-division"),
]:
    register_model(model_class, urlpath_label)
