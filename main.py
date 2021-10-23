import asyncio
import os
import discord
import socket
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv
from github import Github
import time

from Printer import Printer
from PrinterManager import PrinterManager
from Rules import Rules
from EventManager import EventManager
from SpaceManager import SpaceManager
from Sheets import Sheet

from fastapi import FastAPI

#if __name__ == "__main__":  # These variables are used in the functions, must be declared at beginning.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
embedDefaultColor = int(os.getenv('embedDefaultColor'), 16)
bot = commands.Bot(command_prefix=os.getenv('command_prefix'))
events = EventManager()
person_list = SpaceManager()
printersManager = PrinterManager()
printersManager.addPrinter(Printer(name='Hangar Printer', model='Prusa MK3s'))
max_occupancy = int(os.getenv('max_occupancy'))
Sheets = Sheet(os.getenv('SPREADSHEET_ID'))

app = FastAPI()


@app.get("{printerip}")
def recieveIP(printerip):
    print(f"Recieved printerip: {printerip}")

@bot.event
async def on_ready():
    """
    Code to run when the bot first connects to Discord
    :return: None
    """
    print('Program connected')
    #await person_list.reset()
    await person_list.readFromFile()


@bot.event
async def on_command_error(ctx, error):
    """
    When an incorrect command is sent or an exception is raised in a command, send an error message.
    :param ctx: context of the message
    :param error: the error
    :return: None
    """
    print(error)
    await ctx.reply(error)
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

"""
@bot.command(name='checkin', help='Checks you into the DBF space.')
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
        person_list.occupants.append(ctx.message.author.display_name)

        await ctx.reply('You are all checked in! Welcome to the DBF space!')


@bot.command(name='checkout', help='Checks you out the DBF space.')
async def checkout(ctx):
    if ctx.message.author.display_name in person_list.occupants:
        person_list.occupants.remove(ctx.message.author.display_name)
        await person_list.write_to_log(ctx, False, False)
        await ctx.reply('You are all checked out! Thanks for visiting the DBF space!')
    else:
        await ctx.reply("You aren't checked in!")


@bot.command(name='getlog', help='Returns a text file with checkins and checkouts')
async def getlog(ctx):
    await person_list.return_file(ctx)


@bot.command(name='resetlog', help='Resets the log of checkins and checkouts')
async def resetlog(ctx):
    if str(ctx.message.author.id) in person_list.ppltonotify:
        await person_list.reset()
        await ctx.reply("The log has been reset")
    else:
        await ctx.reply("You do not have permissions to perform this action")
"""

@bot.command(name='rules', help='Sends the DBF rules for a particular year')
async def rules(ctx, year: str):
    """
    Replies with the rules for the specified year
    :param ctx: context of the message
    :param year: year for rules
    :return: None
    """
    try:
        rulesEmbed = discord.Embed(title=f"{year} rules", color=embedDefaultColor)
        rulesEmbed.description = f"[**Click here**]({Rules.years[int(year)]})"
        await ctx.reply(embed=rulesEmbed)
    except KeyError:
        await ctx.reply(f"We do not have rules for the year {year} in our database")


@bot.command(name='remindme', help='Creates a future event with a specific message.')
async def remindme(ctx, message: str, time: str):
    """
    Creates a new event
    :param ctx: context of the message
    :param message: What message to send
    :param time: What time to send the message
    :return: None
    """
    await events.addEvent(ctx, message, time)


@bot.command(name='delete', help='Deletes an event. Ex: <delete 2>. Use list command to get event numbers.')
async def delete(ctx, eventKey: str):
    """
    Deletes an Event
    :param ctx: context of the message
    :param eventKey: The hash of the Event to be deleted
    :return: None
    """
    isAdmin = str(ctx.message.author.id) in person_list.ppltonotify  # Could have a more official list of Admins.
    isAuthor = ctx.message.author == events.dictionary[int(eventKey)].ctx.message.author
    if isAdmin or isAuthor:
        try:
            events.removeEventByKey(int(eventKey))
            await ctx.reply('Event deleted.')
        except KeyError:
            await ctx.reply('That event was not found.')
        except ValueError:
            await ctx.reply('Please enter the number from the list of the reminder you would like to delete')
    else:
        await ctx.reply('You are not authorized to delete that message.')


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
    isAdmin = str(ctx.message.author.id) in person_list.ppltonotify
    if isAdmin:
        amount = events.numEvents()
        events.clearEvents()
        await ctx.send(str(amount) + ' event(s) cleared. There are now no upcoming events.')
    else:
        await ctx.reply("You are not authorized to perform that command.")


@bot.command(name='printers', help='Returns the current ip address of the Octoprint server')
async def printers(ctx):
    """
    Sends a list of all printers and their Octopi's IP address. Should work with more than one, but not yet tested.
    :param ctx: context of the message
    :return: None
    """
    ipEmbed = discord.Embed(title='__**Printers**__', description=f"```prolog\n{printersManager.getList()}\n```",
                            color=embedDefaultColor)
    await ctx.reply(embed=ipEmbed)


@bot.command(name='order', help='Submits a request to purchase an item.')
async def Order(ctx, item, price, quantity, url):
    """
    Submits an item to the DBF request form.
    :param ctx: the context of the message
    :param item: name of the item
    :param price: price
    :param quantity: quantity
    :param url: url at which it can be purchased
    :return: None
    """
    Sheets.sendToSheet(item, price, quantity, url, ctx)
    await ctx.reply(f"Done! {item} added to spreadsheet.")


@bot.command(name='spreadsheet', help='Returns the url of the spreadsheet')
async def Spreadsheet(ctx):
    """
    Responds with the url of the DBF request form spreadsheet.
    :param ctx: context of the message
    :return: None
    """
    await ctx.reply(f"Here it is: {Sheets.url()}")


async def notifyPeople(ctx):
    """
    Sends a Direct Message to club leadership that too many people are in the space
    :param ctx: context of the message
    :return: None
    """
    for person in person_list.ppltonotify:
        converter = commands.MemberConverter()
        member = await converter.convert(ctx, person)
        await member.send("The space is over capacity!")


if __name__ == '__main__':  # This must run after the functions are declared
    bot.run(TOKEN)
