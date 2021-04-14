import discord
from discord.ext import commands
import os.path
from os import path
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv


class SpaceManager:
    def __init__(self) -> object:
        self.occupants = []
        self.ppltonotify = []
        self.readFromFile()
        load_dotenv()
        self.timezone = os.getenv("deployTimezone")
        with open("DBF Space Log.txt", "w") as doc:
            doc.write("This Log of the Design Build Fly Space was created at ")
            current_date_time = str(datetime.now(pytz.timezone(self.timezone)))
            doc.write(f"{current_date_time}\n")

    async def return_file(self, ctx):
        with open('DBF Space Log.txt', 'r') as fp:
            current_date_time = str(datetime.now(pytz.timezone(self.timezone)))
            current_date_time = f'{current_date_time[0:13]}.{current_date_time[14:16]}.{current_date_time[17:19]}'
            await ctx.reply(file=discord.File(fp, f'DBF Space Log {current_date_time}.txt'))

    def write_to_log(self, ctx, is_checking_in, is_over_capacity):
        with open("DBF Space Log.txt", "a") as doc:
            checkin_or_out = ''
            over_capacity = ''
            if is_checking_in:
                checkin_or_out = 'checked into the space at'
            else:
                checkin_or_out = 'checked out of the space at'
            if is_over_capacity:
                over_capacity = "The Space is over capacity!"
            to_write = f"{ctx.message.author.display_name} {checkin_or_out} "
            to_write += f"{datetime.now(pytz.timezone(self.timezone))}. {over_capacity}\n"
            doc.write(to_write)

    def readFromFile(self):
        peopleString = ""
        if path.exists('ppltonotify.txt'):
            if os.stat('ppltonotify.txt').st_size != 0:
                with open('ppltonotify.txt', 'r') as people:
                    peopleString = people.read()
                self.ppltonotify = peopleString.split('\n')
        return
