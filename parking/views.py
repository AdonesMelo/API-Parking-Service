from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets

from core.permissions import IsOwnerOfVehicleOrRecord

from parking.filters import ParkingFilterClass, ParkingSpotFilterClass
from parking.models import ParkingSpot, ParkingRecord
from parking.serializers import ParkingSpotSerializer, ParkingRecordSerializer


class ParkingSpotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
    rql_filter_class = ParkingSpotFilterClass
    permission_classes = [DjangoModelPermissions]


class ParkingRecordViewSet(viewsets.ModelViewSet):
    queryset = ParkingRecord.objects.all()
    serializer_class = ParkingRecordSerializer
    # rql_filter_class = ParkingFilterClass
    permission_classes = [DjangoModelPermissions, IsOwnerOfVehicleOrRecord]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ParkingRecord.objects.none()
        
        user = self.request.user
        if not user.is_authenticated:
            return ParkingRecord.objects.none()
        
        if user.is_staff:
            return ParkingRecord.objects.select_related('vehicle', 'parking_spot').all()
        return ParkingRecord.objects.select_related('vehicle', 'parking_spot').filter(vehicle__owner__user=user)
