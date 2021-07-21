from rest_framework.routers import (
    DynamicRoute,
    SimpleRouter,
)


class SocialRouter(SimpleRouter):
    # Views for creating and retrieving social content: comments, votes/likes
    routes = [
        DynamicRoute(
            url=r"^{prefix}/{lookup}/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            detail=False,
            initkwargs={},
        )
    ]
