from typing import List


class MessagePool():
    def __init__(self, user: int):
        self.user = user
        self.messages = []


class NotificationsPool(object):
    """Manage users and message for the grpc server"""

    def __init__(self):
        # for quickly check validations
        # multiple grpc connections share same messages pool
        self._users: List[int] = []
        self._message_pool: List[MessagePool] = []

    def has_user(self, user: int) -> bool:
        """Check if a user already has a connection"""
        return user in self._users

    def add_user(self, user: int) -> None:
        """Add a user to the notifications pool"""
        if self.has_user(user):
            return
        self._users.append(user)
        # self._message_pool.append({'user': user, 'messages': []})
        self._message_pool.append(MessagePool(user=user))

    def remove_user(self, user: int) -> None:
        """Remove a user from the notifications pool"""
        if not self.has_user(user):
            return
        self._users.remove(user)
        index = -1
        for i, pool in enumerate(self._message_pool):
            if pool.user == user:
                index = i
                break
        if index != -1:
            self._message_pool.pop(index)

    def user_messages(self, user: int) -> List[str]:
        """Returns user messages list"""
        # if not self.has_user(user):
        #    return []
        for pool in self._message_pool:
            if pool.user == user:
                return pool.messages
        else:
            return []

    def add_user_message(self, user: int, message: str) -> None:
        for pool in self._message_pool:
            if pool.user == user:
                pool.messages.append(message)
                return

    def remove_user_messages(self, user: int, messages: List[str]) -> None:
        """Remove a user messages"""
        for pool in self._message_pool:
            if pool.user == user:
                for message in messages:
                    try:
                        pool.messages.remove(message)
                    except ValueError:
                        pass
                return
