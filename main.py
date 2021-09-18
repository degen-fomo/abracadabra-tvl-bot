#Based off of juliankoh/ribbon-discord-bot/bot_tvl.py


import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
REFRESH_TIMER = os.getenv('REFRESH_TIMER')


client = discord.Client()

def get_tvl():
    r = requests.get("https://analytics.abracadabra.money/api/statistic/tvl").json()
    tvl = round(r['tvl'] / 1000000, 1)
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
        await guild.me.edit(nick=get_tvl())
client.run(TOKEN)