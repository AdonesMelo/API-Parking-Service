from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets

from core.permissions import IsOwnerOfVehicleOrRecord

from vehicles.filters import VehicleTypeFilterClass, VehicleFilterClass
from vehicles.models import VehicleType, Vehicle
from vehicles.serializers import VehicleTypeSerializer, VehicleSerializer


class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    rql_filter_class = VehicleTypeFilterClass
    permission_classes = [DjangoModelPermissions, IsAdminUser]


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    #rql_filter_class = VehicleFilterClass
    permission_classes = [DjangoModelPermissions, IsOwnerOfVehicleOrRecord]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Vehicle.objects.none()
        
        user = self.request.user
        if not user.is_authenticated:
            return Vehicle.objects.none()
        
        if user.is_staff:
            return Vehicle.objects.select_related('vehicle_type', 'owner').all()
        return Vehicle.objects.select_related('vehicle_type', 'owner').filter(owner__user=user)
