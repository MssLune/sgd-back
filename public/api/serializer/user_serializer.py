import os

from django.db import transaction
from rest_framework import serializers, validators

from ...models import User
from ..serializer.group_serializer import GroupSerializer
from sgd.constants import ROLE
from utils.validators import number_validator


class LoginUserSerializer(serializers.ModelSerializer):
    # Serializer used in custom token response
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'photo',
            'groups'
        ]

    def to_representation(self, instance):
        # Add url to photo
        ret = super().to_representation(instance)
        if 'photo' in self.fields:
            ret['photo'] = os.environ.get('MEDIA_URL_LOGIN') + ret['photo']
        return ret


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'photo']


class ClientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'gender', 'phone', 'email',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        password = self.validated_data.get('password')
        self.validated_data['username'] = self.validated_data['email']
        with transaction.atomic():
            instance = User(**self.validated_data)
            instance.set_password(password)
            instance.save()
            instance.groups.set([ROLE.CLIENT])

            return instance
