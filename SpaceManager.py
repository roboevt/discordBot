import discord
from discord.ext import commands
import os.path
from os import path
import os


class SpaceManager:
    def __init__(self):
        self.movements = []
        self.occupants = []
        self.ppltonotify = []
        self.readFromFile()

    @staticmethod
    async def return_file(ctx):
        with open('archive.txt', 'r') as fp:
            await ctx.send(file=discord.File(fp, 'archive.txt'))

    def synchronize(self):
        # print("In sync")
        with open('archive.txt', 'w') as fp:
            to_add = ''
            for movement in self.movements:
                # print("in loop")
                to_add += movement.toString() + "\n"
                # print("after to_add")
            fp.write(to_add)
        return

    def readFromFile(self):
        peopleString = ""
        if path.exists('ppltonotify.txt'):
            if os.stat('ppltonotify.txt').st_size != 0:
                with open('ppltonotify.txt', 'r') as people:
                    peopleString = people.read()
                self.ppltonotify = peopleString.split('\n')

        return
