from dj_rql.drf import RQLFilterBackend

from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets

from customers.filters import CustomerFilterClass
from customers.models import Customer
from customers.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = CustomerFilterClass
    # Permiçao para usuario admin e do back office, para criar, editar e deletar clientes
    permission_classes = [DjangoModelPermissions, IsAdminUser]
