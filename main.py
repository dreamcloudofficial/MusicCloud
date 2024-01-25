from dotenv import load_dotenv
load_dotenv()

import discord
import os
from discord.ext import commands
from pytube import YouTube

bot = commands.Bot(command_prefix = "$", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command()
async def play(ctx: commands.Context):
    user = ctx.message.author
    voice_channel = user.voice.channel

    channel = None

    if voice_channel != None:
        channel = voice_channel

        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio("gilld chese.mp3"))

bot.run(os.getenv("TOKEN"))
