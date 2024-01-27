from urllib.parse import quote
from discord.ext import commands
import requests

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @commands.command()
    async def gpt(ctx: commands.Context, *prompt: str):
        prompt = " ".join(prompt)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        gpt_prompt = requests.get(f"https://api.gglvxd.eu.org/v2/chatgpt?q={quote(prompt)}", headers = headers)

        await ctx.send(gpt_prompt.json()["chat"])

async def setup(bot):
    await bot.add_cog(AI(bot))