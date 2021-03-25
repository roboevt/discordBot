# bot.py
import asyncio
import os

from discord.ext import commands
from dotenv import load_dotenv

from Event import Event
from Rules import Rules

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='test2', help='responds with "test success!" if the bot is running correctly.')
async def test(ctx):
    await ctx.send('test 2 success!')


@bot.command(name='rules', help='sends the DBF rules for a particular year')
async def test(ctx, year):
    if year.isdigit():
        year = int(year)
        if year in Rules.years:
            await ctx.send(Rules.years[year])
        else:
            await ctx.send('We do not have the year ' + str(year) + ' in our database, please try another year.')
    else:
        await ctx.send('Please input the year as an integer, for example, "rules 2016"')


@bot.command(name='create', help='Creates an event in future. Input a message to be sent, and when to send it')
async def reminder(ctx, message, year, month, day, hour, minute):
    event = Event.checkArgs(message, year, month, day, hour, minute)  # returns an error message or an Event object
    if isinstance(event, str):
        await ctx.send(event)
    else:
        await ctx.send('message received, sending follow up after ' + str(round(event.secondsLeft(), 0)) + ' seconds')
        await delayedSend(ctx, event)


async def delayedSend(ctx, event):
    Event.list_of_events.append(event)
    await asyncio.sleep(event.secondsLeft())
    await ctx.send(event.message)
    Event.list_of_events.remove(event)


bot.run(TOKEN)
