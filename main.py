import asyncio
from dotenv import load_dotenv
load_dotenv()

import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
@bot.event
async def on_ready():
    print("Bot is ready!")

class CloudHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(title = ":question: Help", description = page, color = 0xe82711)
            await destination.send(embed = embed)

bot.help_command = CloudHelp()

cogfiles = [
    f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs/") if filename.endswith(".py")
]

async def load_cogs():
    for cogfile in cogfiles:
        await bot.load_extension(cogfile)

asyncio.run(load_cogs())
bot.run(os.getenv("TOKEN"))