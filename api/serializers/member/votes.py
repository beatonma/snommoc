from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer
from api.serializers.divisions.votes import (
    CommonsVotesSerializer,
    LordsVotesSerializer,
)
from repository.models import (
    CommonsDivisionVote,
    LordsDivisionMemberVote,
    Person,
)


class MemberVotesSerializer(DetailedModelSerializer):
    """Votes by a Person, ordered with most recent first."""

    commons = serializers.SerializerMethodField()
    lords = serializers.SerializerMethodField()

    def get_commons(self, person):
        return self._get(person, CommonsDivisionVote, CommonsVotesSerializer)

    def get_lords(self, person):
        return self._get(person, LordsDivisionMemberVote, LordsVotesSerializer)

    def _get(self, person, model, serializer_model):
        qset = (
            model.objects.filter(person=person)
            .prefetch_related("division")
            .order_by("-division__date")
        )
        return serializer_model(qset, many=True).data

    class Meta:
        model = Person
        fields = [
            contract.HOUSE_COMMONS,
            contract.HOUSE_LORDS,
        ]
