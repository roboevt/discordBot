# bot.py
import asyncio
import os
import discord
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv

from Event import Event
from Rules import Rules
from EventManager import EventManager
from SpaceManager import SpaceManager
from Movement import Movement

if __name__ == "__main__":
    print('in setup')
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    embedDefaultColor = os.getenv('embedDefaultColor')
    bot = commands.Bot(command_prefix=os.getenv('command_prefix'))
    print(os.getenv('command_prefix'))
    events = EventManager()
    person_list = SpaceManager()
    max_occupancy = os.getenv('max_occupancy')


@bot.event
async def on_ready():
    print('Program started')
    #for eventToSend in events.eventsList:
    #    await delayedSend(eventToSend)


"""@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That command is not recognized, please try again.')
    if isinstance(error, commands.BadArgument) \
            or isinstance(error, commands.MissingRequiredArgument) \
            or isinstance(error, commands.ArgumentParsingError) \
            or isinstance(error, commands.TooManyArguments) \
            or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('There was an issue with the parameters of that command. Check !help for more information')
"""

@bot.command(name='test', help='responds with "test success!" if the bot is running correctly.')
async def test2(ctx):
    await ctx.send('test success!')


@bot.command(name='checkin', help='Lets people check into the DBF space.')
async def checkin(ctx):
    if ctx.message.author.display_name in person_list.occupants:
        await ctx.send("You're already checked in!")
    else:
        if len(person_list.occupants) >= max_occupancy:
            print("too many people")
            await notifyPeople(ctx)
            await ctx.send("Warning: There are already " + str(len(person_list.occupants)) +
                           " people in the space! There can only be " + str(max_occupancy) + " people at a time!")
        move = Movement(ctx.message.author.display_name, True)
        person_list.movements.append(move)
        person_list.occupants.append(ctx.message.author.display_name)
        person_list.synchronize()
        await ctx.send('You are all checked in! Welcome to the DBF space!')


@bot.command(name='checkout', help='Lets people check out the DBF space.')
async def checkin(ctx):
    if ctx.message.author.display_name in person_list.occupants:
        move = Movement(ctx.message.author.display_name, False)
        person_list.movements.append(move)
        person_list.occupants.remove(ctx.message.author.display_name)
        person_list.synchronize()
        await ctx.send('You are all checked out! Thanks for visiting the DBF space!')
    else:
        await ctx.send("You aren't checked in!")


@bot.command(name='resetarchive', help='Resets the recent archive')
async def resetarchive(ctx):
    global person_list
    person_list = SpaceManager()
    with open('bigarchive.txt', 'a') as fp:
        to_add = "The short term archive was reset at " + datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        fp.write(to_add)
    await ctx.send('The short term archive was reset')


@bot.command(name='getdetailedarchive',
             help='Returns a text file with all recorded checkins and checkouts as well as recent archive resets')
async def getspacelogs(ctx):
    with open('bigarchive.txt', 'r') as fp:
        await ctx.send(file=discord.File(fp, 'detailedArchive.txt'))


@bot.command(name='getrecentarchive', help='Returns a text file with checkins and checkouts')
async def getspacelogs(ctx):
    await person_list.return_file(ctx)


@bot.command(name='rules', help='sends the DBF rules for a particular year')
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
async def create(ctx, message, time):
    await events.addEvent(ctx, message, time)


@bot.command(name='delete', help='Deletes an event. Ex: !delete 2. Use !list to get event numbers.')
async def delete(ctx, eventKey):
    try:
        events.deleteEvent(eventKey)
        await ctx.send('Event deleted.')
    except KeyError:
        await ctx.send('That event was not found.')
    except ValueError:
        await ctx.send('Please enter the number from the list of the reminder you would like to delete')


@bot.command(name='list', help='Lists all upcoming events with message and time')
async def listEvents(ctx):
    listEmbed = discord.Embed(title='Upcoming events:', description=events.listEvents(), color=0x00aff4)#change color bacl
    await ctx.send(embed=listEmbed)


@bot.command(name='clear', help='Clears all upcoming events')
async def clear(ctx):
    amount = events.numEvents()
    events.clearEvents()
    await ctx.send(str(amount) + ' event(s) cleared. There are now 0 upcoming events.')


async def notifyPeople(ctx):
    for person in person_list.ppltonotify:
        converter = commands.MemberConverter()
        member = await converter.convert(ctx, person)
        await member.send("The space is over capacity!")


if __name__ == '__main__':
    bot.run(TOKEN)
