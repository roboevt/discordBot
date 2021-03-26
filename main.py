# bot.py
import asyncio
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

from Event import Event
from Rules import Rules
from EventManager import EventManager

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
embedDefaultColor = 0x00aff4

bot = commands.Bot(command_prefix='!')

events = EventManager()


@bot.event
async def on_ready():
    print('Program started')
    for eventToSend in events.eventsList:
        await delayedSend(eventToSend)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That command is not recognized, please try again.')
    if isinstance(error, commands.BadArgument) \
            or isinstance(error, commands.MissingRequiredArgument) \
            or isinstance(error, commands.ArgumentParsingError) \
            or isinstance(error, commands.TooManyArguments) \
            or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('There was an issue with the parameters of that command. Check !help for more information')


@bot.command(name='test2', help='responds with "test success!" if the bot is running correctly.')
async def test(ctx):
    await ctx.send('test 2 success!')


@bot.command(name='rules2', help='sends the DBF rules for a particular year')
async def rules(ctx, year):
    if year.isdigit():
        year = int(year)
        if year in Rules.years:
            rulesEmbed = discord.Embed(title=str(year) + ' rules:', color=embedDefaultColor)
            rulesEmbed.description = '[**Click here**](' + Rules.years[year] + ')'
            await ctx.send(embed=rulesEmbed)
            print('Sent rules for year ' + year)
            # await ctx.send('__**' + str(year) + ' rules:**__\n' + Rules.years[year])
        else:
            await ctx.send('We do not have the year ' + str(year) + ' in our database, please try another year.')
    else:
        await ctx.send('Please input the year as an integer, for example, "rules 2016"')


@bot.command(name='create', help='Creates a future event with a specific message.')
async def reminder(ctx, message, year, month, day, hour, minute):
    event = Event.checkArgs(ctx.channel.id, message, year, month, day, hour, minute)
    if isinstance(event, str):  # if checkArgs() returned an error string, send it
        await ctx.send(event)
    else:  # if it did not return a string, it returned a new Event object, so process that
        events.addEvent(event)
        await ctx.send('message received, sending follow up after ' + str(round(event.secondsLeft(), 0)) + ' seconds')
        await delayedSend(event)


@bot.command(name='delete', help='Deletes an event. Ex: !delete 2. Use !list to get event numbers.')
async def delete(ctx, numberToDelete):
    if numberToDelete.isdigit():
        numberToDelete = int(numberToDelete)
    for eventToDelete in events.eventsList:
        if eventToDelete.number == numberToDelete:
            await ctx.send('Event ' + str(eventToDelete.number) + ' with message "' + eventToDelete.message + '" deleted.')
            events.removeEvent(eventToDelete)
            return
    await ctx.send('That event was not found. Use the "list" command to see event numbers.')


@bot.command(name='list', help='Lists all upcoming events with message and time')
async def listEvents(ctx):
    stringEvents = events.listEvents()
    listEmbed = discord.Embed(title='Upcoming events:', description=stringEvents, color=embedDefaultColor)
    await ctx.send(embed=listEmbed)
    # await ctx.send('>>> '+ stringEvents)


@bot.command(name='clear', help='Clears all upcoming events')
async def clear(ctx):
    amount = len(events.eventsList)
    events.clearEvents()
    await ctx.send(str(amount) + ' event(s) cleared. There are now 0 upcoming events.')


async def delayedSend(event):
    time = event.secondsLeft()
    if time > 0:
        await asyncio.sleep(event.secondsLeft())
        await bot.get_channel(event.channelID).send(event.message)
        print('sending: ' + event.message)
    events.removeEvent(event)


bot.run(TOKEN)
