import logging

from django.db import models
from django.db.models import QuerySet

from common.cache import invalidate_cache as invalidate_cache_impl

log = logging.getLogger(__name__)


class InvalidateCacheQuerySet(QuerySet):
    def update(self, *, invalidate_cache: bool = False, **kwargs):
        result = super().update(**kwargs)
        if invalidate_cache:
            self.model.invalidate_cache()
        return result

    def delete(self, invalidate_cache: bool = False):
        result = super().delete()
        if invalidate_cache:
            self.model.invalidate_cache()
        return result


class InvalidateCacheMixin(models.Model):
    """Invalidate caches tagged with `cache_key` whenever the model is saved.

    Example usage:
        @decorate_view(cache_page(60 * 60, key_prefix=MyCachedModel.cache_key))
        def my_view...
    """

    class Meta:
        abstract = True

    cache_key: str

    def save(
        self,
        *args,
        invalidate_cache: bool = True,
        **kwargs,
    ):
        super().save(*args, **kwargs)
        if invalidate_cache:
            self.invalidate_cache()

    def delete(self, *args, invalidate_cache: bool = True, **kwargs):
        super().delete(*args, **kwargs)
        if invalidate_cache:
            self.invalidate_cache()

    @classmethod
    def invalidate_cache(cls):
        invalidate_cache_impl(cls.cache_key)
