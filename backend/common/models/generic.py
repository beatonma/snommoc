from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class GenericTargetMixin(models.Model):
    target_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey("target_type", "target_id")

    @staticmethod
    def get_target_kwargs(target: models.Model) -> dict:
        return {
            "target_type": ContentType.objects.get_for_model(target),
            "target_id": target.pk,
        }

    class Meta:
        abstract = True
