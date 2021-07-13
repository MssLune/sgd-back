from rest_framework import viewsets

from ...models import Service
from ..serializer.service_serializer import ServiceSerializer
from sgd.constants import ROLE
from utils import permissions as custom_permissions


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [custom_permissions.HasGroupPermission]
    permission_groups = {
        'list': [custom_permissions.IS_AUTHENTICATED],
        'retrieve': [custom_permissions.IS_AUTHENTICATED]
    }
