from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

from dashboard.views.dashboard import StaffView
from repository.models import (
    Bill,
    CommonsDivision,
    Constituency,
    LordsDivision,
    Party,
    Person,
)
from repository.models.util.queryset import get_or_none
from surface.models import FeaturedBill, FeaturedCommonsDivision, FeaturedLordsDivision, FeaturedPerson


class DashboardSearch(StaffView):
    def get(self, request, *args, **kwargs):
        query = kwargs.get('query')

        results = {
            'Person': _for_named_model(Person, query, 'member-detail', FeaturedModel=FeaturedPerson),
            'Party': _for_named_model(Party, query, 'party-detail'),
            'Constituency': _for_named_model(Constituency, query, 'constituency-detail'),
            'Bill': _for_titled_model(Bill, query, 'bill-detail', FeaturedModel=FeaturedBill),
            'CommonsDivision': _for_titled_model(CommonsDivision, query, 'division/commons-detail',
                                                 FeaturedModel=FeaturedCommonsDivision),
            'LordsDivision': _for_titled_model(LordsDivision, query, 'division/lords-detail',
                                               FeaturedModel=FeaturedLordsDivision),
        }

        return JsonResponse(data=results)


def _for_named_model(Model, query, pathname, FeaturedModel=None) -> list:
    results = Model.objects.filter(Q(name__icontains=query))[:5]

    return [
        _result(
            name=x.name,
            url=reverse(pathname, args=[x.pk]),
            id=x.pk,
            featured=_check_is_featured(FeaturedModel, x),
        ) for x in results
    ]


def _for_titled_model(Model, query, pathname, FeaturedModel=None) -> list:
    results = Model.objects.filter(Q(title__icontains=query))[:5]
    return [
        _result(
            name=x.title,
            url=reverse(pathname, args=[x.pk]),
            id=x.pk,
            featured=_check_is_featured(FeaturedModel, x),
        ) for x in results
    ]


def _result(name, url, id, featured) -> dict:
    return {
        'name': name,
        'url': url,
        'id': id,
        'featured': featured,
    }


def _check_is_featured(FeaturedModel, obj):
    """
    :param FeaturedModel: [surface.models.BaseFeatured] model type that represents a featured instance of the object.
    """
    if FeaturedModel is None:
        return None
    else:
        target = get_or_none(FeaturedModel, target_id=obj.pk)

        return target is not None
