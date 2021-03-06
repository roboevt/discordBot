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

bot.run(TOKEN)