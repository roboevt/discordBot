import asyncio
from datetime import datetime
import jsonpickle


class Event(object):

    def __init__(self, ctx, message, time):
        self.ctx = ctx
        self.message = message
        self.time = time

    def __eq__(self, other):
        return all((self.ctx == other.ctx, self.message == other.message, self.time == other.time))

    def __hash__(self):
        return abs(hash((self.ctx, self.message, self.time)))  # Is this ok?
        # Is more legible but might not always be unique...

    def toJsonPickle(self):
        return jsonpickle.encode(self)

    def timeRemaining(self):
        return self.time - datetime.now()

    async def delayedSend(self, timeOut):
        await asyncio.sleep(timeOut)
        await self.ctx.send(self.message)
