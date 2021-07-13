import datetime

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...models import User, Service, ScheduledService


class _UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'photo']


class _ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']


class ScheduledServiceAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledService
        fields = '__all__'


class ScheduledServiceListClientSerializer(serializers.ModelSerializer):
    technician = _UserSerializer()
    service = _ServiceSerializer()

    class Meta:
        model = ScheduledService
        fields = [
            'id', 'service', 'technician', 'date', 'time', 'gradable'
        ]


class ScheduledServiceRetrieveClientSerializer(serializers.ModelSerializer):
    technician = _UserSerializer()
    service = _ServiceSerializer()

    class Meta:
        model = ScheduledService
        fields = [
            'id', 'service', 'technician', 'date', 'time', 'address',
            'reference', 'gradable'
        ]


class ScheduledServiceListTechSerializer(serializers.ModelSerializer):
    client = _UserSerializer()
    service = _ServiceSerializer()

    class Meta:
        model = ScheduledService
        fields = [
            'id', 'service', 'client', 'date', 'time'
        ]


class ScheduledServiceRetrieveTechSerializer(serializers.ModelSerializer):
    client = _UserSerializer()
    service = _ServiceSerializer()

    class Meta:
        model = ScheduledService
        fields = [
            'id', 'service', 'client', 'date', 'time', 'address', 'reference',
            'latitude', 'longitude'
        ]


class ScheduledServiceCreateSerializer(serializers.ModelSerializer):
    client = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = ScheduledService
        fields = [
            'id', 'service', 'client', 'technician', 'date', 'time', 'address',
            'latitude', 'longitude', 'reference'
        ]

    def validate_time(self, value: datetime.time):
        min_time = datetime.time(5, 0)
        max_time = datetime.time(22, 0)
        if value <= min_time or value >= max_time:
            raise ValidationError(
                'La hora se encuentra fuera del horario de servicio.')
        return value

    def validate(self, data):
        date = data.get('date')
        time = data.get('time')
        technician = data.get('technician')
        plus_delta = timezone.timedelta(hours=1)
        less_delta = timezone.timedelta(minutes=30)
        min_time = (datetime.datetime.combine(date, time) - less_delta).time()
        max_time = (datetime.datetime.combine(date, time) + plus_delta).time()
        if ScheduledService.objects.filter(
                technician=technician,
                date=date,
                time__range=(min_time, max_time)).exists():
            raise ValidationError(
                'El técnico ya cuenta con un servicio apartado para la hora '
                'y fecha enviados.')
        return data

    def create(self, validated_data):
        return ScheduledService.objects.create(**validated_data)
