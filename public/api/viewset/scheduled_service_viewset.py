from rest_framework import viewsets

from ...models import ScheduledService
from ..serializer.scheduled_service_serializer import (
    ScheduledServiceListClientSerializer,
    ScheduledServiceRetrieveClientSerializer,
    ScheduledServiceListTechSerializer,
    ScheduledServiceRetrieveTechSerializer,
    ScheduledServiceAdminSerializer,
    ScheduledServiceCreateSerializer
)
from sgd.constants import ROLE
from utils import permissions as custom_permissions


class ScheduledServiceViewSet(viewsets.ModelViewSet):
    queryset = ScheduledService.objects.all()
    permission_classes = [custom_permissions.HasGroupPermission]
    permission_groups = {
        'list': [custom_permissions.IS_AUTHENTICATED],
        'retrieve': [custom_permissions.IS_AUTHENTICATED],
        'create': [ROLE.CLIENT],
        'partial_update': [custom_permissions]
    }
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.request.user.is_anonymous:  # For schema generation
            return ScheduledServiceListClientSerializer
        if self.request.user.in_group([ROLE.CLIENT]):
            if self.action == 'list':
                return ScheduledServiceListClientSerializer
            elif self.action == 'retrieve':
                return ScheduledServiceRetrieveClientSerializer
            elif self.action == 'create':
                return ScheduledServiceCreateSerializer
        elif self.request.user.in_group([ROLE.TECHNICIAN]):
            if self.action == 'list':
                return ScheduledServiceListTechSerializer
            elif self.action == 'retrieve':
                return ScheduledServiceRetrieveTechSerializer
        elif self.request.user.in_group([ROLE.ADMIN]):
            return ScheduledServiceAdminSerializer
        return ScheduledServiceListClientSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.in_group([ROLE.ADMIN]):
            queryset = queryset.all()
        elif self.request.user.in_group([ROLE.CLIENT]):
            queryset = queryset.filter(client=self.request.user)\
                .select_related('calification')
        elif self.request.user.in_group([ROLE.TECHNICIAN]):
            queryset = queryset.filter(technician=self.request.user)
        else:
            queryset = queryset.none()
        return queryset.select_related('client', 'technician', 'service')
