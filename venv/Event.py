from datetime import datetime

class Event:
    list_of_events = []
    def __init__(self, message, time):
        self.message=message
        self.time=time

    @classmethod
    def fromDateArgs(event, message, year, month, day, hour, minute):
        return event(message, datetime(year, month, day, hour, minute, 0))

    @staticmethod
    def checkArgs(message, year, month, day, hour, minute):
        if year.isdigit:
            year=int(year)
        else:
            return 'You must enter an integer for year.'
        if month.isdigit:
            month=int(month)
            if not 0<=month<=12:
                return 'The month must be from 0 to 12.'
        else:
            return 'You must enter an integer for month'
        if day.isdigit:
            day=int(day)
            if not 0<=day<=31:
                return 'The day must be from 0 to 31.'
        else:
            return 'You must enter an integer for day.'
        if hour.isdigit:
            hour=int(hour)
            if not 0<=hour<=24:
                return 'The hour must be from 0 to 24.'
        else:
            return 'You must enter an integer for hour.'
        if minute.isdigit:
            minute=int(minute)
            if not 0<=minute<=60:
                return 'The minute must be from 0 to 60.'
        else:
            return 'You must enter an integer for minute.'

        time=datetime(year, month, day, hour, minute, 0)
        if time.timestamp() - datetime.now().timestamp() < 0:
            return 'That time is in the past, please enter a time in the future.'

        return Event(message, year, month, day, hour, minute)

    def secondsLeft(self):
        return self.time.timestamp() - datetime.now().timestamp()