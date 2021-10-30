from Printer import Printer


class PrinterManager(object):
    def __init__(self):
        self.printerList = []

    def addPrinter(self, printerDetails: str):
        printerDetails = printerDetails.split(',')
        for printer in self.printerList:
            if printer.name == printerDetails[0] and printer.model == printerDetails[1]:
                printer.ip = printerDetails[2]
                return
        self.printerList.append(Printer(printerDetails[0], printerDetails[1], printerDetails[2]))

    def getList(self):
        printerString = ''
        if len(self.printerList) == 0:
            printerString = 'None'
        for printer in self.printerList:
            printerString += f"Name:`{printer.name}`\nModel:`{printer.model}`\tIP:{printer.getIp()}\n"
        return printerString

    def clearList(self):
        self.printerList.clear()

#rest semantics
#with forms
#don't use commas to seperate data
