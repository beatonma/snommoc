from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer
from api.serializers.inline import InlineConstituencySerializer
from api.serializers.member.address import AddressSerializer
from api.serializers.member.committees import CommitteeMemberSerializer
from api.serializers.member.constituencies import HistoricalConstituencySerializer
from api.serializers.member.declared_interests import DeclaredInterestSerializer
from api.serializers.member.experiences import ExperienceSerializer
from api.serializers.member.house_memberships import HouseMembershipSerializer
from api.serializers.member.maiden_speeches import MaidenSpeechSerializer
from api.serializers.member.party_associations import HistoricalPartySerializer
from api.serializers.member.posts import AllPostSerializer
from api.serializers.member.subjects_of_interest import SubjectOfInterestSerializer
from api.serializers.member.town import TownSerializer
from api.serializers.parties import InlinePartySerializer
from repository.models import Person


class SimpleProfileSerializer(DetailedModelSerializer):
    """Return basic information about a Member."""

    party = InlinePartySerializer()
    constituency = InlineConstituencySerializer()
    portrait = serializers.URLField(source="memberportrait.wide_url")

    class Meta:
        model = Person
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.MEMBER_NAME,
            contract.ACTIVE,
            contract.PARTY,
            contract.CONSTITUENCY,
            contract.IS_MP,
            contract.IS_LORD,
            contract.PORTRAIT,
            contract.CURRENT_POST,
        ]


class _DetailedProfileSerializer(DetailedModelSerializer):
    """Return basic information about a Member."""

    party = InlinePartySerializer()
    constituency = InlineConstituencySerializer()
    place_of_birth = TownSerializer(source="town_of_birth")
    portrait = serializers.URLField(source="memberportrait.wide_url")

    class Meta:
        model = Person
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.MEMBER_NAME,
            contract.MEMBER_TITLE,
            contract.GIVEN_NAME,
            contract.FAMILY_NAME,
            contract.ACTIVE,
            contract.THEYWORKFORYOU,
            contract.PARTY,
            contract.CONSTITUENCY,
            contract.IS_MP,
            contract.IS_LORD,
            contract.DATE_OF_BIRTH,
            contract.DATE_OF_DEATH,
            contract.AGE,
            contract.GENDER,
            contract.PLACE_OF_BIRTH,
            contract.PORTRAIT,
            contract.CURRENT_POST,
        ]


class FullMemberSerializer(DetailedModelSerializer):
    """Return a full profile with all data for a Person."""

    profile = _DetailedProfileSerializer(source="*")
    address = AddressSerializer(source="*")
    committees = CommitteeMemberSerializer(many=True, source="committeemember_set")
    constituencies = HistoricalConstituencySerializer(
        many=True, source="constituencyresult_set"
    )
    experiences = ExperienceSerializer(many=True, source="experience_set")
    houses = HouseMembershipSerializer(many=True, source="housemembership_set")
    interests = DeclaredInterestSerializer(many=True, source="declaredinterest_set")
    parties = HistoricalPartySerializer(many=True)
    posts = AllPostSerializer(source="*")
    speeches = MaidenSpeechSerializer(many=True, source="maidenspeech_set")
    subjects = SubjectOfInterestSerializer(many=True, source="subjectofinterest_set")

    class Meta:
        model = Person
        fields = [
            contract.PROFILE,
            contract.ADDRESS,
            contract.COMMITTEES,
            contract.HISTORICAL_CONSTITUENCIES,
            contract.EXPERIENCES,
            contract.HOUSES,
            contract.FINANCIAL_INTERESTS,
            contract.MAIDEN_SPEECHES,
            contract.PARTY_ASSOCIATIONS,
            contract.POSTS,
            contract.SUBJECTS_OF_INTEREST,
        ]
