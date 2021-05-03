from typing import Optional
from fuzzywuzzy import fuzz

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
from surface.models import (
    FeaturedBill,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
    FeaturedPerson,
)


class DashboardSearch(StaffView):
    def get(self, request, *args, **kwargs):
        query = kwargs.get("query")

        people = _for_named_model(
            Person, query, "member-detail", FeaturedModel=FeaturedPerson
        )
        parties = _for_named_model(Party, query, "party-detail")
        constituencies = _for_named_model(Constituency, query, "constituency-detail")

        bills = _for_titled_model(
            Bill, query, "bill-detail", FeaturedModel=FeaturedBill
        )

        commonsdivisions = _for_titled_model(
            CommonsDivision,
            query,
            "division/commons-detail",
            FeaturedModel=FeaturedCommonsDivision,
        )

        lordsdivisions = _for_titled_model(
            LordsDivision,
            query,
            "division/lords-detail",
            FeaturedModel=FeaturedLordsDivision,
        )

        results = (
            people
            + parties
            + constituencies
            + bills
            + commonsdivisions
            + lordsdivisions
        )[:20]

        results.sort(key=lambda item: (item["score"]), reverse=True)

        return JsonResponse(data={"results": results})


def _for_named_model(Model, query, pathname, FeaturedModel=None) -> list:
    results = Model.objects.filter(Q(name__icontains=query) | Q(pk__contains=query))[
        :20
    ]

    return [
        _result(
            type=Model.__name__,
            name=x.name,
            url=reverse(pathname, args=[x.pk]),
            id=x.pk,
            featured=_check_is_featured(FeaturedModel, x),
            start=_get_date(x, "start"),
            end=_get_date(x, "end"),
            date=_get_date(x, "date"),
            score=_score(query, x.name),
        )
        for x in results
    ]


def _for_titled_model(Model, query, pathname, FeaturedModel=None) -> list:
    results = Model.objects.filter(Q(title__icontains=query) | Q(pk__contains=query))[
        :20
    ]
    return [
        _result(
            type=Model.__name__,
            name=x.title,
            url=reverse(pathname, args=[x.pk]),
            id=x.pk,
            featured=_check_is_featured(FeaturedModel, x),
            start=_get_date(x, "start"),
            end=_get_date(x, "end"),
            date=_get_date(x, "date"),
            score=_score(query, x.title),
        )
        for x in results
    ]


def _get_date(obj, attr) -> Optional[str]:
    date = getattr(obj, attr, None)
    if date is None:
        return None

    return date.isoformat()


def _result(type, name, url, id, featured, start, end, date, score) -> dict:
    return {
        "type": type,
        "name": name,
        "url": url,
        "id": id,
        "featured": featured,
        "start": start,
        "end": end,
        "date": date,
        "score": score,
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


def _score(*args):
    return fuzz.token_set_ratio(*args)
