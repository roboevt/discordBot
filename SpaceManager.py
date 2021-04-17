import discord
from discord.ext import commands
import os.path
from os import path
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
import aiofiles


class SpaceManager:
    def __init__(self) -> object:
        self.occupants = []
        self.ppltonotify = []
        load_dotenv()
        self.timezone = os.getenv("discordTimezone")
        self.file_name = ''

    async def return_file(self, ctx):
        current_date_time = str(datetime.now(pytz.timezone(self.timezone)))
        current_date_time = f'{current_date_time[0:13]}.{current_date_time[14:16]}.{current_date_time[17:19]}'
        await ctx.reply(file=discord.File(self.file_name, f'DBF Space Log {current_date_time}.txt'))

    async def write_to_log(self, ctx, is_checking_in, is_over_capacity):
        async with aiofiles.open(self.file_name, "a") as doc:
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
            await doc.write(to_write)

    async def reset(self):
        current_date_time = str(datetime.now(pytz.timezone(self.timezone)))
        current_date_time = f'{current_date_time[0:13]}.{current_date_time[14:16]}.{current_date_time[17:19]}'
        self.file_name = f"DBF Space Log {current_date_time}.txt"
        async with aiofiles.open(self.file_name, "w") as doc:
            await doc.write("This Log of the Design Build Fly Space was created at ")
            current_date_time = str(datetime.now(pytz.timezone(self.timezone)))
            await doc.write(f"{current_date_time}\n")

    async def readFromFile(self):
        peopleString = ""
        if path.exists('ppltonotify.txt'):
            if os.stat('ppltonotify.txt').st_size != 0:
                async with aiofiles.open('ppltonotify.txt', 'r') as people:
                    peopleString = await people.read()
                self.ppltonotify = peopleString.split('\n')
        return
    # Since this only runs at the very beginning and init runs it, I am not making this async
