import discord
import os
import requests
import json
import random
import asyncio
import logging
from discord.ext import commands
from discord.ext.context import ctx
from discord.voice_client import VoiceClient
from replit import db
from keep_alive import keep_alive
import music




client = discord.Client()
intents = discord.Intents.all()

client = commands.Bot(command_prefix = "$", intents=intents)

my_secret = os.environ['Private']

#music bot:

cogs = [music]

for i in range(len(cogs)):
  cogs[i].setup(client)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.command()
async def ping(ctx):
    await ctx.send(f"pong {round(client.latency * 1000)}ms")
    server = ctx.message.author.guild
    server_name = server.name
    server_id = server.id
    server_owner = server.owner.name
    await ctx.send("server name: {}\n"
          "server id: {}\n"
          "server owner: {}"
          .format(server_name, server_id, server_owner))
    try:
        # Create target Directory
        os.mkdir(str(server.name))
        print("Guild Directory ", str(server.name),  " Created ") 
    except FileExistsError:pass
        #print("Guild Directory ", str(server.name),  " already exists")

    with open(str(server.name) + "\\" + str(server.name) + "_info.json", "w") as s:
        e = "Server name: " + server.name + "\n" + "Server ID: " + str(server_id) + "\n" + "Server Owner: " + server_owner
        #print(e)
        s.write(e)
        s.close()
  

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


#welcome message
@client.event
async def on_member_join(member):
  mbed = discord.Embed(
    colour = (discord.Colour.magenta()),
    title = 'Sunucuma hoş geldin canım arkadaşımız 🥰',
    description = f' Sunucumuza normalde çok insan almayız ve almamız da seni özel gördüğümüz anlamına gelir, umarım eğlenirsin {member.mention}, eğer bir problem olursa ferivonus a haber verebilirsin 😣'
  )
  await member.send(embed=mbed)
  print("log in worked")
  channel = discord.utils.get(member.guild.channels, name='genel')
  embed=discord.Embed(colour = (discord.Colour.magenta()),title="Sunucuya yeni birisi geldi!", description = f"hoş geldin {member.mention}, aramıza katılabileceğine eminim, umarım çok mutlu olursun ve aramızda yerinin olduğunu hissedebilirsin 🥰")
  await channel.send(embed=embed)
  print("log in worked")

#goodbye message
@client.event

async def on_member_remove(member):
  mbed = discord.Embed(
    colour = (discord.Colour.magenta()),
    title = 'Gittiğin için çok üzgünüz...',
    description = f' Sunucumuzdan çıkma nedenini anlayamasamda benim çözebileceğim bir şey varsa lütfen ferivonusa haber ver, problem yaşamak ya da üzgün bir insan kalsın istiyorum, umarım çok mutlu olursun, {member.mention} kendine iyi bak 😔'
    )
  await member.send(embed = mbed)
  print("log out worked")
  channel = discord.utils.get(member.guild.channels, name='genel')
  embed=discord.Embed(colour = (discord.Colour.magenta()),title="Aramızdan birisi ayrıldı...", description = f"Gitti... {member.mention}, aramızdan ayrıldı... Neden çıktığını sorabilen var mı? öğrenmem gerekiyor gibi hissediyorum, umarım çok bir şey olmamıştır... 😞")
  await channel.send(embed=embed)
  print("log out worked")
  


keep_alive()
client.run(my_secret)


