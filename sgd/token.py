from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from public.api.serializer.user_serializer import LoginUserSerializer


class CustomObtainPairView(TokenObtainPairView):
    """
    Ovewrite the `TokenObtainPairView.post` method for add user information\n
    to response and update user last_login.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        data = serializer.validated_data
        data['user'] = LoginUserSerializer(serializer.user).data
        serializer.user.last_login = timezone.localtime()
        serializer.user.save()

        return Response(data=data, status=status.HTTP_200_OK)
