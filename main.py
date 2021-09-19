#Based off of juliankoh/ribbon-discord-bot/bot_tvl.py


import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import requests
import json
import aiohttp

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
REFRESH_TIMER = os.getenv('REFRESH_TIMER')


client = discord.Client()

async def get_tvl():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://analytics.abracadabra.money/api/statistic/tvl") as r:
            if r.status == 200:
                js = await r.json()
                tvl = round(js['tvl'] / 1000000, 1)
                tvlstring = (f"TVL: ${tvl}M")
                return tvlstring

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord! ')
    for guild in client.guilds:
        print("connected to ", guild.name)
    refresh_tvl.start()

@tasks.loop(seconds=float(REFRESH_TIMER))
async def refresh_tvl():
    for guild in client.guilds:
        await guild.me.edit(nick=await get_tvl())
client.run(TOKEN)