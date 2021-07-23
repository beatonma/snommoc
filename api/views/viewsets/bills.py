from api.serializers.bills import BillSerializer
from api.views.viewsets import KeyRequiredViewSet
from repository.models import Bill


class BillViewSet(KeyRequiredViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
