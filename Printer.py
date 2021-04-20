import os
from dotenv import load_dotenv
from github import Github


class Printer(object):

    def __init__(self, name='defaultName', model='defaultModel', ip='0.0.0.0'):
        load_dotenv()
        self.name = name
        self.model = model
        self.ip = ip
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.repository = self.github.get_user().get_repo('discordBotPrinter')

    def getIp(self):
        self.ip = self.repository.get_contents('printerip.txt').decoded_content.decode()
        return self.ip
