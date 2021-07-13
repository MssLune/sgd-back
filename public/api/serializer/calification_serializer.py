from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...models import Calification, ScheduledService


class CalificationSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(
        max_length=255, allow_blank=True, required=False)

    class Meta:
        model = Calification
        fields = '__all__'

    def validate(self, data):
        scheduled_service = data.get('scheduled_service')
        if scheduled_service.status != ScheduledService.Status.COMPLETED:
            raise ValidationError(
                'No puede calificar un servicio que no se haya completado')
        return data
