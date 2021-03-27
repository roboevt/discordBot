import os
from datetime import datetime
import Event
import pickle


class EventManager:
    def __init__(self):
        self.eventsList = []
        self.readFromFile()
        self.sortEvents()
        self.checkEvents()

    def addEvent(self, event):
        print(event.toString() + ' added to list')
        self.eventsList.append(event)
        self.sortEvents()
        self.saveToFile()

    def removeEvent(self, event):
        try:
            self.eventsList.remove(event)
            print(event.toString() + ' removed from list')
        except ValueError:  # if the event isn't in the list
            return  # then it's already removed, no need to worry (maybe come back to this)
        self.sortEvents()
        self.saveToFile()

    def sortEvents(self):
        print('Sorting ' + str(len(self.eventsList)) + ' event(s).')
        self.eventsList.sort(key=lambda eventToSort: eventToSort.time)
        i = 0
        for event in self.eventsList:
            i += 1
            event.number = i

    def listEvents(self):
        if len(self.eventsList) != 0:
            # eventString = '__**Upcoming events:**__ \n'
            eventString = ''
            for event in self.eventsList:
                eventString += str(event.number) + ':\t'
                eventString += '*' + event.message + '*'
                eventString += '\t'
                eventString += event.time.strftime("%m/%d/%Y, %H:%M:%S")
                eventString += '\n\n'
            eventString += ''
            return eventString
        else:
            return 'No upcoming events.'

    def clearEvents(self):
        print(str(len(self.eventsList)) + ' event(s) cleared')
        self.eventsList.clear()

    def checkEvents(self):
        for eventToCheck in self.eventsList:
            if eventToCheck.secondsLeft() < 0:
                print('Event missed during down time: ' + eventToCheck.toString())
                self.removeEvent(eventToCheck)

    def saveToFile(self):
        print('Saved ' + str(len(self.eventsList)) + ' event(s) to file.')
        self.sortEvents()
        with open('events.p', 'wb') as outFile:
            pickle.dump(self.eventsList, outFile)

    def readFromFile(self):
        if os.stat('events.p').st_size != 0:
            with open('events.p', 'rb') as inFile:
                self.eventsList = pickle.load(inFile)
            print(str(len(self.eventsList)) + ' event(s) read from file.')
            self.sortEvents()
