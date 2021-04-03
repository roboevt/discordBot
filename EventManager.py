from datetime import datetime
import dateparser
from dotenv import load_dotenv
import os
import pytz
from Event import Event
import asyncio


class EventManager(object):
    def __init__(self):
        self.dictionary = {}
        load_dotenv()
        self.timezone = os.getenv('timezone')

    async def addEvent(self, ctx, message, time: datetime):
        time = dateparser.parse(time, settings={'TIMEZONE': self.timezone})
        time = pytz.timezone(self.timezone).localize(time)
        eventAdded = Event(ctx, message, time)
        eventAdded.future = asyncio.create_task(self.delayedSend(eventAdded, ctx, message, time))
        print(f"hash: {hash(eventAdded)}")
        self.dictionary[hash(eventAdded)] = eventAdded

    async def delayedSend(self, event: Event, ctx, message, time):
        now = datetime.now(pytz.timezone(self.timezone))
        timeDeltaSend = time - now
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
