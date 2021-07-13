from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ...models import User
from ..serializer.user_serializer import (
    UserListSerializer,
    ClientSerializer
)
from sgd.constants import ROLE
from utils import permissions as custom_permissiosn


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [custom_permissiosn.HasGroupPermission]
    permission_groups = {
        'list': [ROLE.ADMIN],
        'retrieve': [ROLE.ADMIN],
        'create': [ROLE.ADMIN],
        'partial_update': [custom_permissiosn.IS_AUTHENTICATED],
        'client': [custom_permissiosn.ALLOW_ANY],
        'technicians': [custom_permissiosn.IS_AUTHENTICATED],
    }

    def get_serializer_class(self):
        if self.request.user.is_anonymous:
            if self.action == 'client':
                return ClientSerializer
        return UserListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'technicians':
            service = int(self.request.query_params.get('service'))
            return queryset.filter(
                groups=ROLE.TECHNICIAN, services=service)
        if self.request.user.in_group([ROLE.ADMIN]):
            return queryset
        return queryset.filter(pk=self.request.user.id)

    @action(methods=['post'], detail=False, url_path='client')
    def client(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='technicians')
    def technicians(self, request):
        service = request.query_params.get('service')
        if service is None or not service.isdigit():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().list(request=request)
