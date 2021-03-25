from datetime import datetime

class Event:
    def __init__(self, message, time):
        self.message=message
        self.time=time

    @classmethod
    def fromDateArgs(event, message, year, month, day, hour, minute):
        valid=True
        if year.isdigit:
            year=int(year)
        else:
            valid=False
        if month.isdigit:
            month=int(month)
        else:
            valid = False
        if day.isdigit:
            day=int(day)
        else:
            valid = False
        if hour.isdigit:
            hour=int(hour)
        else:
            valid = False
        if minute.isdigit:
            minute=int(minute)
        else:
            valid = False
        if valid:
            return event(message, datetime(year, month, day, hour, minute, 0))
        else:
            print("Invalid date entered.")


    def secondsLeft(self):
        return self.time.timestamp() - datetime.now().timestamp()