from datetime import datetime
import dateparser
import pytz
from Event import Event
import asyncio


class EventManager(object):
    def __init__(self):
        self.dictionary = {}

    async def addEvent(self, ctx, message, time: datetime):
        time = dateparser.parse(time, settings={'TIMEZONE': 'America/Chicago'})
        eventAdded = Event(ctx, message, time)
        eventAdded.future = asyncio.create_task(self.delayedSend(eventAdded, ctx, message, time))
        print(f"hash: {hash(eventAdded)}")
        self.dictionary[hash(eventAdded)] = eventAdded

    async def delayedSend(self, event: Event, ctx, message, time):
        print(1)
        CST = pytz.timezone('America/Chicago')
        print(2)
        timeDeltaSend = time - datetime.now(CST)
        print(3)
        print(timeDeltaSend.total_seconds())
        print(f"sending followup in {timeDeltaSend.total_seconds()}")
        await asyncio.sleep(timeDeltaSend.total_seconds())
        print('sending followup')
        await ctx.send(message)
        self.removeEvent(event)

    def removeEvent(self, event: Event) -> None:
        event.future.cancel()
        del self.dictionary[hash(event)]

    def listEvents(self):
        eventString = ''
        if len(self.dictionary) == 0:
            eventString = 'None'
        for event in self.dictionary.items():
            eventString += f"\nID: {hash(event[1])} \t Date: {event[1].time.strftime('%m/%d/%Y %H:%M')}" \
                           f"\nMessage: '{event[1].message}'\n"
        return eventString

    def deleteEvent(self, eventKey: int):
        print(self.dictionary)
        self.removeEvent(self.dictionary[int(eventKey)])

    def numEvents(self) -> int:
        return len(self.dictionary)

    def clearEvents(self):
        self.dictionary.clear()
