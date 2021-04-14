import asyncio
from datetime import datetime, timedelta


class Event(object):

    def __init__(self, ctx, message: str, time: datetime):
        """
        Initializes a new Event
        :param ctx: context of the message (which server/channel to send response to)
        :param message: The message to send
        :param time: The datetime the message should be sent at
        """
        self.ctx = ctx
        self.message = message
        self.time = time
        self.future = None

    def __eq__(self, other):
        """
        Checks if this Event is equivalent to another one.
        :param other: The other Event to check against
        :return: Boolean
        """
        return all((self.ctx == other.ctx, self.message == other.message, self.time == other.time))

    def __hash__(self):
        """
        Hashes this event
        :return: int
        """
        return abs(hash((self.ctx, self.message, self.time)))
