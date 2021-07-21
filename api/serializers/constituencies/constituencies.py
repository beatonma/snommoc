from api import contract
from api.serializers.base import DetailedModelSerializer
from api.serializers.constituencies.boundary import ConstituencyBoundarySerializer
from api.serializers.constituencies.election_results import ElectionResultSerializer
from api.serializers.inline import InlineMemberSerializer
from repository.models import Constituency


class ConstituencySerializer(DetailedModelSerializer):
    mp = InlineMemberSerializer()
    boundary = ConstituencyBoundarySerializer(source="constituencyboundary")
    results = ElectionResultSerializer(source="constituencyresult_set", many=True)

    class Meta:
        model = Constituency
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
            contract.MP,
            contract.START,
            contract.END,
            contract.CONSTITUENCY_BOUNDARY,
            contract.CONSTITUENCY_RESULTS,
        ]
