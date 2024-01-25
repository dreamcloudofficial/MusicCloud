from dotenv import load_dotenv
load_dotenv()

import discord
import os
from discord.ext import commands
from pytube import YouTube

bot = commands.Bot(command_prefix = "=", intents = discord.Intents.all())
@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command()
async def play(ctx: commands.Context, url: str):
    user = ctx.message.author
    voice_channel = user.voice.channel

    global voice_client
    voice_client = ctx.guild.voice_client

    channel = None

    if not voice_client in bot.voice_clients:
        channel = voice_channel
    else:
        channel = voice_client

    if voice_channel != None:
        yt = YouTube(url)
        song = yt.streams.filter(only_audio=True).first()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        if voice_client in bot.voice_clients:
            vc = channel
        else:
            vc = await channel.connect()

        vc.play(discord.FFmpegPCMAudio(song.url, **FFMPEG_OPTIONS))
        await ctx.send(f"Playing {yt.title}")

@bot.command()
async def stop(ctx: commands.Context):
    user = ctx.message.author
    voice_channel = user.voice.channel

    global voice_client
    voice_client = ctx.guild.voice_client

    channel = None

    if not voice_client in bot.voice_clients:
        channel = voice_channel
    else:
        channel = voice_client

    if voice_channel != None:
        if voice_client in bot.voice_clients:
            vc = channel
        else:
            vc = await channel.connect()
        
        vc.stop()
        await ctx.send(f"Stopping song.")

bot.run(os.getenv("TOKEN"))
