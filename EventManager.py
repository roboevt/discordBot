import os
from datetime import datetime
import Event
import pickle


class EventManager:
    def __init__(self):
        self.eventsList = []
        self.readFromFile()
        self.checkEvents()

    def addEvent(self, event):
        self.eventsList.append(event)
        self.saveToFile()

    def removeEvent(self, event):
        try:
            self.eventsList.remove(event)
        except ValueError:
            return
        self.saveToFile()

    def listEvents(self):
        if len(self.eventsList) != 0:
            eventString = '__**Upcoming events:**__ \n'
            for event in self.eventsList:
                eventString += '*'+event.message+'*'
                eventString += ' '
                eventString += event.time.strftime("%m/%d/%Y, %H:%M:%S")
                eventString += '\n'
            return eventString
        else:
            return 'No upcoming events.'

    def clearEvents(self):
        self.eventsList.clear()

    def checkEvents(self):
        for eventToCheck in self.eventsList:
            if eventToCheck.secondsLeft()<0:
                self.removeEvent(eventToCheck)

    def saveToFile(self):
        with open('events.p', 'wb') as outFile:
            pickle.dump(self.eventsList, outFile)

    def readFromFile(self):
        if os.stat('events.p').st_size != 0:
            with open('events.p', 'rb') as inFile:
                self.eventsList = pickle.load(inFile)
