import discord
import os
import requests
import json
import random
import asyncio
import logging
from discord.ext import commands
from discord.voice_client import VoiceClient
from replit import db
from keep_alive import keep_alive


intents = discord.Intents.all()
client = discord.Client()

client = commands.Bot(command_prefix = "!", intents=intents)

my_secret = os.environ['Private']

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


#welcome message
@client.event
async def on_member_join(member):
  channel = discord.utils.get(member.guild.channels, name='genel')
  await channel.send(f"Hoş geldin {member.mention}  umarım çok eğlenirsin.")
  await member.send(f"Hoş geldin {member.mention} umarım çok eğlenirsin.")
  

#goodbye message
@client.event
async def on_member_remove(member):
  channel = discord.utils.get(member.guild.channels, name='genel')
  await channel.send(f'Arkadaşlar {member.mention} çıktı, haberiniz olsun!')
  await member.send(f'Arkadaşlar {member.mention} çıktı, haberiniz olsun!')


keep_alive()
client.run(my_secret)


