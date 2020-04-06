"""

"""

import logging

from api.serializers import (
    AddressSerializer,
    AllPostSerializer,
    DetailedModelSerializer,
    ExperienceSerializer,
    CommitteeMemberSerializer,
    DeclaredInterestSerializer,
    InlinePartySerializer,
    InlineConstituencySerializer,
)
from api.serializers.constituencies import HistoricalConstituencySerializer
from api.serializers.house_memberships import HouseMembershipSerializer
from api.serializers.inline import InlineTownSerializer
from api.serializers.maiden_speeches import MaidenSpeechSerializer
from api.serializers.parties import HistoricalPartySerializer
from api.serializers.subjects_of_interest import SubjectOfInterestSerializer
from repository.models import Person

from rest_framework import serializers

log = logging.getLogger(__name__)


class SimpleProfileSerializer(DetailedModelSerializer):
    """Return basic information about a Member."""
    party = InlinePartySerializer()
    constituency = InlineConstituencySerializer()
    place_of_birth = InlineTownSerializer(source='town_of_birth')
    portrait = serializers.URLField(source='memberportrait.wide_url')

    class Meta:
        model = Person
        fields = [
            'parliamentdotuk',
            'name',
            'full_title',
            'given_name',
            'family_name',
            'active',
            'theyworkforyou',
            'party',
            'constituency',
            'is_mp',
            'is_lord',
            'date_of_birth',
            'date_of_death',
            'age',
            'gender',
            'place_of_birth',
            'portrait',
            'current_post',
        ]


class FullProfileSerializer(DetailedModelSerializer):
    """Return a full profile with all data for a Person."""
    profile = SimpleProfileSerializer(source='*')
    address = AddressSerializer(source='*')
    committees = CommitteeMemberSerializer(many=True, source='committeemember_set')
    constituencies = HistoricalConstituencySerializer(many=True, source='constituencyresult_set')
    experiences = ExperienceSerializer(many=True, source='experience_set')
    houses = HouseMembershipSerializer(many=True, source='housemembership_set')
    interests = DeclaredInterestSerializer(many=True, source='declaredinterest_set')
    parties = HistoricalPartySerializer(many=True)
    posts = AllPostSerializer(source='*')
    speeches = MaidenSpeechSerializer(many=True, source='maidenspeech_set')
    subjects = SubjectOfInterestSerializer(many=True, source='subjectofinterest_set')

    class Meta:
        model = Person
        fields = [
            'profile',
            'address',
            'committees',
            'constituencies',
            'experiences',
            'houses',
            'interests',
            'speeches',
            'parties',
            'posts',
            'subjects',
        ]
