from typing import List

from django.urls import reverse
from rest_framework import serializers

from dashboard.views.scoring import get_similarity_score
from repository.models.constituency import get_suggested_constituencies
from repository.models import Constituency, UnlinkedConstituency


class UnlinkedConstituencySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk")
    url = serializers.SerializerMethodField()
    person = serializers.SerializerMethodField()
    election = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse("admin:repository_unlinkedconstituency_change", args=[obj.pk])

    def get_person(self, obj):
        return {
            "name": obj.person.name,
            "url": reverse("member-detail", args=[obj.person.pk]),
        }

    def get_election(self, obj):
        return {
            "name": obj.election.name,
            "url": reverse("admin:repository_election_change", args=[obj.election.pk]),
            "date": obj.election.date,
        }

    class Meta:
        model = UnlinkedConstituency
        fields = [
            "id",
            "name",
            "url",
            "person",
            "election",
        ]


class UnlinkedConstituencyDetailedSerializer(UnlinkedConstituencySerializer):
    suggestions = serializers.SerializerMethodField()

    def get_suggestions(self, obj):
        suggestions = _get_suggested_constituencies(obj)
        return [
            {
                "id": x.pk,
                "name": x.name,
                "url": reverse("constituency-detail", args=[x.pk]),
                "start": x.start,
                "end": x.end,
                "score": get_similarity_score(obj.name, x.name),
            }
            for x in suggestions
        ]

    class Meta:
        model = UnlinkedConstituency
        fields = [
            "name",
            "url",
            "person",
            "election",
            "suggestions",
        ]


def _get_suggested_constituencies(unlinked: UnlinkedConstituency) -> List[Constituency]:
    return get_suggested_constituencies(unlinked.name, unlinked.election.date)
