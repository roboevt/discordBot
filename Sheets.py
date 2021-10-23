from __future__ import print_function
import os.path

import httplib2
from googleapiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account


class Sheet(object):
    def __init__(self, SPREADSHEET_ID):  # Mainly code from the google sheets python quickstart, could be improved.
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SPREADSHEET_ID = SPREADSHEET_ID
        self.credentials = service_account.Credentials.from_service_account_file('service_key.json', scopes=self.SCOPES)
        self.service = discovery.build('sheets', 'v4', credentials=self.credentials)

    def sendToSheet(self, item, price, quantity, url, ctx):
        outValue = [[item, price, quantity, url, str(ctx.author.nick), 'Requested'], []]
        body = {'values': outValue}

        self.service.spreadsheets().values().append(
            spreadsheetId=self.SPREADSHEET_ID, range="A2",
            valueInputOption="RAW", body=body).execute()

    def url(self):
        return 'https://docs.google.com/spreadsheets/d/' + self.SPREADSHEET_ID  # Magic number

#setup cicd - continous integration
#or just extend expiration time