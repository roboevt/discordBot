from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class Sheet(object):
    def __init__(self, SPREADSHEET_ID):
        # If modifying these scopes, delete the file token.json.
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        self.SPREADSHEET_ID = SPREADSHEET_ID

        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = self.flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('sheets', 'v4', credentials=self.creds)

        # Call the Sheets API
        self.sheet = self.service.spreadsheets()

    def sendToSheet(self, item, price, url, ctx):
        outValue = [[item, price, url, str(ctx.author.name)], []]
        body = {
            'values': outValue
        }
        self.service.spreadsheets().values().append(
            spreadsheetId=self.SPREADSHEET_ID, range="A2",
            valueInputOption="RAW", body=body).execute()
