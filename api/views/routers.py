"""

"""

import logging

from rest_framework.routers import (
    SimpleRouter,
    Route
)

log = logging.getLogger(__name__)


class ListOrDetailRouter(SimpleRouter):
    # Read-only list/detail views
    routes = [
        # All objects, simple overview
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={}
        ),
        # Single object, more detailed data
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
    ]


class DetailOnlyRouter(SimpleRouter):
    # Read-only detail views
    routes = [
        # Single object, more detailed data
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
    ]
