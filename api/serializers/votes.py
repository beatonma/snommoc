"""

"""

import logging

from rest_framework import serializers

from api.serializers import (
    DetailedModelSerializer,
    InlineModelSerializer,
)
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    LordsDivision,
    LordsDivisionVote,
    Person,
)

log = logging.getLogger(__name__)


class GenericDivisionSerializer(serializers.Serializer):
    parliamentdotuk = serializers.IntegerField()
    title = serializers.CharField()
    date = serializers.DateField()
    passed = serializers.BooleanField()
    house = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class InlineCommonsDivisionSerializer(InlineModelSerializer):
    class Meta:
        model = CommonsDivision
        fields = [
            'parliamentdotuk',
            'title',
            'date',
            'passed',
        ]


class InlineLordsDivisionSerializer(InlineModelSerializer):
    class Meta:
        model = LordsDivision
        fields = [
            'parliamentdotuk',
            'title',
            'date',
            'passed',
        ]


class CommonsVotesSerializer(InlineModelSerializer):
    division = InlineCommonsDivisionSerializer()

    class Meta:
        model = CommonsDivisionVote
        fields = [
            'division',
            'vote_type',
        ]


class LordsVotesSerializer(InlineModelSerializer):
    division = InlineLordsDivisionSerializer()

    class Meta:
        model = CommonsDivisionVote
        fields = [
            'division',
            'vote_type',
        ]


class MemberVotesSerializer(DetailedModelSerializer):
    """Votes by a Person, ordered with most recent first."""
    commons = serializers.SerializerMethodField()
    lords = serializers.SerializerMethodField()

    def get_commons(self, person):
        return self._get(person, CommonsDivisionVote, CommonsVotesSerializer)

    def get_lords(self, person):
        return self._get(person, LordsDivisionVote, LordsVotesSerializer)

    def _get(self, person, model, serializer_model):
        qset = model.objects.filter(person=person) \
            .prefetch_related('division') \
            .order_by('-division__date')
        return serializer_model(qset, many=True).data

    class Meta:
        model = Person
        fields = [
            'commons',
            'lords',
        ]
