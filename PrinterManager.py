from dotenv import load_dotenv
import os
from github import Github
from Printer import Printer


class PrinterManager(object):
    def __init__(self):
        load_dotenv()
        self.printerList = []

    def addPrinter(self, printer):
        self.printerList.append(printer)

    def getList(self):
        printerString = ''
        if len(self.printerList) == 0:
            printerString = 'None'
        for printer in self.printerList:
            printerString += f"Name:`{printer.name}`\nModel:`{printer.model}`\tIP:{printer.getIp()}\n"
        return printerString
