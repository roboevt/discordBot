from datetime import datetime
import dateparser
import pytz
from Event import Event
import asyncio
from dotenv import load_dotenv
import os


class EventManager(object):
    def __init__(self):
        self.dictionary = {}
        load_dotenv()
        self.timezone = pytz.timezone(os.getenv('timezone'))

    async def addEvent(self, ctx, message: str, time: datetime) -> None:
        """
        Adds a new event to the dictionary, with accurate time
        :param ctx: ctx the message should be sent to
        :type ctx:
        :param message: The message the event will send
        :type message: str
        :param time: the time the message should be sent
        :type time: str
        :return:
        :rtype: None
        """
        time = dateparser.parse(time, settings={'TIMEZONE': 'America/Chicago'})
        time = self.timezone.localize(time)
        eventAdded = Event(ctx, message, time)
        eventAdded.future = asyncio.create_task(self.delayedSend(eventAdded))
        self.dictionary[hash(eventAdded)] = eventAdded

    async def delayedSend(self, event: Event) -> None:
        """
        A callback function to send an event at it's time, after a delay
        :param event: The event to send
        :return: A future
        """
        timeDeltaSend = event.time - datetime.now(self.timezone)
        await asyncio.sleep(timeDeltaSend.total_seconds())
        await event.ctx.send(event.message)
        self.removeEvent(event)

    def removeEvent(self, event: Event) -> None:
        """
        Removes an event from the dictionary
        :param event: The event to be removed
        :return: None
        """
        event.future.cancel()
        del self.dictionary[hash(event)]

    def listEvents(self) -> str:
        """
        Creates a list of all upcoming events
        :return: An str with each event's details listed.
        """
        eventString = ''
        if len(self.dictionary) == 0:
            eventString = 'None'
        for event in self.dictionary.items():
            eventString += f"\nID: {hash(event[1])} \t Date: {event[1].time.strftime('%m/%d/%Y %H:%M')}" \
                           f"\nMessage: '{event[1].message}'\n"
        return eventString

    def deleteEvent(self, eventKey: int) -> None:
        """
        Removes an event based on it's hash
        :param eventKey: The integer hash of the event to be deleted
        :return: None
        """
        print(self.dictionary)
        self.removeEvent(self.dictionary[int(eventKey)])

    def numEvents(self) -> int:
        """
        The number of upcoming events
        :return: The number of events
        """
        return len(self.dictionary)

    def clearEvents(self) -> None:
        """
        Deletes all events
        :return: None
        """
        self.dictionary.clear()
