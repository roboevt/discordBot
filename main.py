# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#@client.event
#async def on_member_join(member):
#    await member.create_dm()
#    await member.dm.channel.send(
#        f'Hi {member.name}, welcome to my Discord server! If you see this, my first Discord bot works!'
#    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content=='!test':
        response='test success!'
        await message.channel.send(response)
    if message.content=='ping':
        await message.channel.send('ping')
    if message.content=='!rules':
        await message.channel.send('there are no rules')


client.run(TOKEN)
