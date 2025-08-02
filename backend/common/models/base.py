from django.db import models
from django.db.models import QuerySet

from util.time import get_now


class BaseQuerySet(QuerySet):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class BaseModel(models.Model):
    """
    All concrete model implementations should extend from this.
    """

    objects = BaseQuerySet.as_manager()
    created_at = models.DateTimeField(default=get_now)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
