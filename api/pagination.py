"""

"""

import logging

from rest_framework.pagination import PageNumberPagination

log = logging.getLogger(__name__)


class DefaultResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100
