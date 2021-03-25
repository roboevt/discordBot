# bot.py
import asyncio
import os
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv

from Event import Event

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
years = {1997: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/1997_dbf_rules.pdf',
         1998: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/1998_dbf_rules.pdf',
         1999: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/1999_dbf_rules.pdf',
         2000: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2000_dbf_rules.pdf',
         2001: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2001_dbf_rules.pdf',
         2002: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2002_dbf_rules.pdf',
         2003: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2003_dbf_rules.pdf',
         2004: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2005-rules.pdf',
         2005: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2005-rules.pdf',
         2006: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2006_dbf_rules.pdf',
         2007: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2007_dbf_rules.pdf',
         2008: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2008_dbf_rules.pdf',
         2009: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2009_dbf_rules.pdf',
         2010: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2010_dbf_rules.pdf',
         2011: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2011_dbf_rules.pdf',
         2012: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2012_dbf_rules.pdf',
         2013: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2013_dbf_rules.pdf',
         2014: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2014_dbf_rules.pdf',
         2015: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2015_dbf_rules.pdf',
         2016: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2016_dbf_rules.pdf',
         2017: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2017.pdf',
         2018: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2018.pdf',
         2019: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2019.pdf',
         2020: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2020.pdf',
         2021: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2021-final-v01.pdf'
         }
list_of_events = []


@bot.command(name='test2', help='responds with "test success!" if the bot is running correctly.')
async def test(ctx):
    await ctx.send('test 2 success!')


@bot.command(name='rules', help='sends the DBF rules for a particular year')
async def test(ctx, year):
    if year.isdigit():
        year = int(year)
        if year in years:
            await ctx.send(years[year])
        else:
            await ctx.send('We do not have the year ' + str(year) + ' in our database, please try another year.')
    else:
        await ctx.send('Please input the year as an integer, for example, "rules 2016"')


@bot.command(name='create', help='Creates an event in future. Input a message to be sent, and when to send it')
async def reminder(ctx, message, year, month, day, hour, minute):
    event = Event.fromDateArgs(message, year, month, day, hour, minute)
    print(event.time)
    if event.secondsLeft() < 0:
        await ctx.send('The time is in the past. Please choose a time that has not yet passed.')
    else:
        await ctx.send('message received, sending follow up after ' + str(round(event.secondsLeft(),0)) + ' seconds')
        await delayedSend(ctx, event)


async def delayedSend(ctx, event):
    list_of_events.append(event)
    await asyncio.sleep(event.secondsLeft())
    await ctx.send(event.message)


bot.run(TOKEN)
