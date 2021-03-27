from datetime import datetime


class Movement:
    def __init__(self, name, is_check_in):
        self.person = name
        self.time = datetime.now()
        self.is_check_in = is_check_in
        with open('bigarchive.txt', 'a') as fp:
            to_add = self.toString() + '\n'
            fp.write(to_add)

    def toString(self):
        if self.is_check_in:
            return str(self.person) + ' checked in at ' + self.time.strftime("%m/%d/%Y %H:%M:%S")
        else:
            return str(self.person) + ' checked out at ' + self.time.strftime("%m/%d/%Y %H:%M:%S")
