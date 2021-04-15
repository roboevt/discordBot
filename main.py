import os
import discord
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv

from Rules import Rules
from EventManager import EventManager
from SpaceManager import SpaceManager

if __name__ == "__main__":  # These are used in the functions, must be declared at beginning.
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    embedDefaultColor = int(os.getenv('embedDefaultColor'), 16)
    bot = commands.Bot(command_prefix=os.getenv('command_prefix'))
    events = EventManager()
    person_list = SpaceManager()
    max_occupancy = int(os.getenv('max_occupancy'))


@bot.event
async def on_ready():
    """
    Code to run when the bot first connects to Discord
    :return: None
    """
    print('Program connected')


@bot.event
async def on_command_error(ctx, error):
    """
    When an incorrect command is sent or an exception is raised in a command, send an error message.
    :param ctx: context of the message
    :param error: the error
    :return: None
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply('That command is not recognized, please try again.')
    else:
        await ctx.reply('There was an issue with that command, please check it and try again.')


@bot.command(name='test', help='responds with "test success!" if the bot is running correctly.')
async def test(ctx):
    """
    Responds to the test command with "test success!"
    :param ctx: context of the message
    :return: None
    """
    await ctx.reply('test success!')


@bot.command(name='checkin', help='Lets people check into the DBF space.')
async def checkin(ctx):
    if ctx.message.author.display_name in person_list.occupants:
        await ctx.reply("You're already checked in!")
    else:
        if len(person_list.occupants) >= max_occupancy:
            print("too many people")
            await notifyPeople(ctx)
            await ctx.reply("Warning: There are already " + str(
                len(person_list.occupants)) + " people in the space! There can only be " + str(
                max_occupancy) + " people at a time!")
            await person_list.write_to_log(ctx, True, True)
        else:
            await person_list.write_to_log(ctx, True, False)
        await person_list.occupants.append(ctx.message.author.display_name)

        await ctx.reply('You are all checked in! Welcome to the DBF space!')


@bot.command(name='checkout', help='Lets people check out the DBF space.')
async def checkin(ctx):
    if ctx.message.author.display_name in person_list.occupants:
        await person_list.occupants.remove(ctx.message.author.display_name)
        await person_list.write_to_log(ctx, False, False)
        await ctx.reply('You are all checked out! Thanks for visiting the DBF space!')
    else:
        await ctx.reply("You aren't checked in!")


@bot.command(name='getlog', help='Returns a text file with checkins and checkouts')
async def getlog(ctx):
    await person_list.return_file(ctx)


@bot.command(name='resetlog', help='Resets the log of checkins and checkouts')
async def resetlog(ctx):
    global person_list
    person_list = SpaceManager()
    await ctx.reply("The log has been reset")


@bot.command(name='rules', help='sends the DBF rules for a particular year')
async def rules(ctx, year: str):
    """
    Replies with the rules for the specified year
    :param ctx: context of the message
    :param year: year for rules
    :return: None
    """
    try:
        rulesEmbed = discord.Embed(title=f"{year} rules", color=embedDefaultColor)
        rulesEmbed.description = f"[**Click here**]({Rules.years[year]})"
        await ctx.reply(embed=rulesEmbed)
    except KeyError:
        await ctx.reply(f"We do not have rules for the year {year} in our database")


@bot.command(name='create', help='Creates a future event with a specific message.')
async def create(ctx, message: str, time: str):
    """
    Creates a new event
    :param ctx: context of the message
    :param message: What message to send
    :param time: What time to send the message
    :return: None
    """
    await events.addEvent(ctx, message, time)


@bot.command(name='delete', help='Deletes an event. Ex: !delete 2. Use !list to get event numbers.')
async def delete(ctx, eventKey: str):
    """
    Deletes an Event
    :param ctx: context of the message
    :param eventKey: The hash of the Event to be deleted
    :return: None
    """
    try:
        events.deleteEvent(int(eventKey))
        await ctx.send('Event deleted.')
    except KeyError:
        await ctx.send('That event was not found.')
    except ValueError:
        await ctx.send('Please enter the number from the list of the reminder you would like to delete')


@bot.command(name='list', help='Lists all upcoming events with message and time')
async def listEvents(ctx):
    """
    Creates and sends a discord Embed listing out Events by their hash
    :param ctx: context of the message
    :return: None
    """
    listEmbed = discord.Embed(title='__**Upcoming events:**__', description=f"```prolog\n{events.listEvents()}\n```",
                              color=embedDefaultColor)
    await ctx.reply(embed=listEmbed)


@bot.command(name='clear', help='Clears all upcoming events')
async def clear(ctx):
    """
    Deletes all upcoming Events
    :param ctx: context of the message
    :return: None
    """
    amount = events.numEvents()
    events.clearEvents()
    await ctx.send(str(amount) + ' event(s) cleared. There are now 0 upcoming events.')


async def notifyPeople(ctx):
    for person in person_list.ppltonotify:
        converter = commands.MemberConverter()
        member = await converter.convert(ctx, person)
        await member.send("The space is over capacity!")


if __name__ == '__main__':  # This must run after the functions are declared
    bot.run(TOKEN)
