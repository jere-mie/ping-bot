# this was helpful
# https://discordpy.readthedocs.io/en/latest/faq.html#coroutines

import discord
from discord.ext import commands
import json
import asyncio
import urllib.request
import aiohttp

with open('secrets.json') as f:
    data = json.load(f)

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

@client.command()
async def ping(ctx):
    await ctx.send(f"Latency: {round(client.latency * 1000)}ms")

good = True
async def check2():
    global good
    while not client.is_closed():
        await asyncio.sleep(2)
        channel = client.get_channel(int(data['channel']))
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(data['address']) as r:
                    if r.status == 200:
                        good=True
            except:
                if good:
                    good = False
                    await channel.send("OFFLINE!!!")

client.loop.create_task(check2())
client.run(data['token'])