import os
from dotenv import load_dotenv
from github import Github
from fastapi import FastAPI

app = FastAPI()


class Printer(object):

    def __init__(self, name='defaultName', model='defaultModel', ip='0.0.0.0'):
        load_dotenv()
        self.name = name
        self.model = model
        self.ip = ip
        self.github = Github(os.getenv('GITHUB_TOKEN'))

        self.repository = self.github.get_user().get_repo('discordBotPrinter')

    @app.get("{printerip}")
    async def recieveIP(self, printerip):
        print(f"Recieved printerip: {printerip}")
        self.ip = printerip

    def getIp(self):
        print(f"Returning printerip: {self.ip}")
        return self.ip
