# bot.py
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='test', help='responds with "test success!" if the bot is running correctly.')
async def test(ctx):
    await ctx.send('test success!')

@bot.command(name='rules', help='sends the DBF rules for a particular year')
async def test(ctx, year: int):
    if year == 1997:
        await ctx.send('https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/1997_dbf_rules.pdf')
    if year == 1998:
        await ctx.send('https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/1998_dbf_rules.pdf')
    if year == 1999:
        await ctx.send('https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/1999_dbf_rules.pdf')

bot.run(TOKEN)