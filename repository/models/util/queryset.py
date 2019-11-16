from django.core.exceptions import ObjectDoesNotExist


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def qs_get_or_none(queryset, **kwargs):
    try:
        return queryset.get(**kwargs)
    except ObjectDoesNotExist:
        return None
