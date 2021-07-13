import os

from django.db.models import signals
from django.dispatch import receiver
import grpc

from .models import ScheduledService
from sgd_grpc.proto.sgd_pb2 import SendNotificationRequest as SendRequest
from sgd_grpc.proto.sgd_pb2_grpc import SGDStub


# For more django applications, create the grpc connection in a global scope
addr = os.environ.get('GRPC_ADDRESS', 'localhost:50051')
channel = grpc.insecure_channel(addr)
stub = SGDStub(channel)


@receiver(signals.post_save, sender=ScheduledService, weak=False)
def send_notification(sender, **kwargs):
    created = kwargs.get('created', False)
    if not created:
        return
    instance: ScheduledService = kwargs.get('instance')
    request = SendRequest(
        user=instance.technician_id,
        message='Nuevo servicio solicitado')
    try:
        stub.SendNotification(request)
    except grpc._channel._InactiveRpcError:
        # TODO: move try block to channel declaration
        pass
