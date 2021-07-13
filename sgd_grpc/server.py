import asyncio
import logging
import os
from typing import List, AsyncIterable

import grpc

from proto.sgd_pb2 import (
    OkResponse,
    NotificationRequest,
    NotificationResponse,
    SendNotificationRequest,
    BotRequest,
    BotResponse,
)
from proto.sgd_pb2_grpc import (
    SGDServicer,
    add_SGDServicer_to_server,
)
from sgd_types import NotificationsPool
from chatbot import SGDBot

# TODO: maybe return a uuid type when subscribe to notifications?
# TODO: update NotificationsPool for manage multiple connections
# maybe a counter and when delete message, check that counter.


class SGD(SGDServicer):

    def __init__(self):
        self.notifications_pool = NotificationsPool()
        self.bot = SGDBot

    async def Notifications(
        self,
        request: NotificationRequest,
        context: grpc.aio.ServicerContext
    ) -> AsyncIterable[NotificationResponse]:
        user = request.user
        self.notifications_pool.add_user(user)
        while True:
            message_list = []  # message to remove
            await asyncio.sleep(0.5)
            for message in self.notifications_pool.user_messages(user):
                message_list.append(message)
                yield NotificationResponse(message=message)
            self.notifications_pool.remove_user_messages(user, message_list)

    async def SendNotification(
        self,
        request: SendNotificationRequest,
        context: grpc.aio.ServicerContext
    ) -> OkResponse:
        self.notifications_pool.add_user_message(
            request.user, request.message)
        return OkResponse(ok=True)

    async def Bot(
        self,
        request: BotRequest,
        context: grpc.aio.ServicerContext
    ) -> BotResponse:
        message = str(self.bot.get_response(request.message))
        return BotResponse(message=message)


async def server() -> None:
    server = grpc.aio.server()
    addr = os.environ.get('GRPC_ADDRESS', 'localhost:50051')
    add_SGDServicer_to_server(SGD(), server)
    server.add_insecure_port(addr)
    logging.info('Starting server on %s.' % addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(server())
