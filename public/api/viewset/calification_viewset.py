from rest_framework import viewsets

from ...models import Calification
from ..serializer.calification_serializer import CalificationSerializer
from sgd.constants import ROLE
from utils import permissions as custom_permissions


class CalificationViewSet(viewsets.ModelViewSet):
    queryset = Calification.objects.all()
    serializer_class = CalificationSerializer
    permission_classes = [custom_permissions.HasGroupPermission]
    permission_groups = {
        'list': [ROLE.CLIENT, ROLE.ADMIN],
        'retrieve': [ROLE.ADMIN],
        'create': [ROLE.CLIENT]
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.in_group([ROLE.ADMIN]):
            return queryset
        return queryset.filter(scheduled_service__client=self.request.user)
