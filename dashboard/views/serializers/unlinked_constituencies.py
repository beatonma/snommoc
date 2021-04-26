from django.urls import reverse
from rest_framework import serializers

from repository.models import UnlinkedConstituency


class UnlinkedConstituencySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    mp = serializers.SerializerMethodField()
    election = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('admin:repository_unlinkedconstituency_change', args=[obj.pk])

    def get_mp(self, obj):
        return {
            'name': obj.mp.name,
            'url': reverse('member-detail', args=[obj.mp.pk]),
        }

    def get_election(self, obj):
        return {
            'name': obj.election.name,
            'url': reverse('admin:repository_election_change', args=[obj.election.pk]),
        }

    class Meta:
        model = UnlinkedConstituency
        fields = [
            'name',
            'url',
            'mp',
            'election',
        ]
