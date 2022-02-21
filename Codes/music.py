import asyncio

import discord
from discord.ext import commands
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
  def __init__(self, source, *, data, volume=0.5):
    super().__init__(source, volume)

    self.data = data

    self.title = data.get('title')
    self.url = data.get('url')

  @classmethod
  async def from_url(cls, url, *, loop=None, stream=False):
    loop = loop or asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

    if 'entries' in data:
      # take first item from a playlist
      data = data['entries'][0]

    filename = data['url'] if stream else ytdl.prepare_filename(data)
    return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



class music(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command()
  async def join(slef,ctx):
    if ctx.author.voice is None:
      await ctx.send("You are not in a voice channel...")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

  @commands.command()
  async def disconnect(slef,ctx):
    await ctx.voice_client.disconnect()
  
  @commands.command()
  async def pause(self,ctx):
    await ctx.voice_client.pause()
    await ctx.send("The music is paused")


  @commands.command()
  async def resume(self,ctx):
    await ctx.voice_client.resume()
    await ctx.send("The music is resuming")
    
def setup(client):
  client.add_cog(music(client))