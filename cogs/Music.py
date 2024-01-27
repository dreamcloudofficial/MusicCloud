from discord.ext import commands
import discord
import validators
from pytube import YouTube
from youtube_search import YoutubeSearch

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @commands.command()
    async def play(self, ctx: commands.Context, *url: str):
        url = " ".join(url)
        user = ctx.message.author
        voice_channel = user.voice.channel

        global voice_client
        voice_client = ctx.guild.voice_client

        global channel
        channel = None

        if not voice_client in self.bot.voice_clients:
            channel = voice_channel
        else:
            channel = voice_client

        if voice_channel != None:
            global FFMPEG_OPTIONS
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
            if voice_client in self.bot.voice_clients:
                vc = channel
            else:
                vc = await channel.connect()
        
        if validators.url(url):
            try:
                yt = YouTube(url)
                song = yt.streams.filter(only_audio = True).first()

                vc.play(discord.FFmpegPCMAudio(song.url, **FFMPEG_OPTIONS))
                song_embed = discord.Embed(title = f"Playing {yt.title}", color = 0xbbff00)
                song_embed.set_image(url = yt.thumbnail_url)

                await ctx.send(embed = song_embed)
            except Exception:
                vc.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
                await ctx.send(embed = discord.Embed(title = f"Playing <{url}>", color = 0xae00ff))
        else:
            results = YoutubeSearch(url, max_results = 1).to_dict()
            search_yt = YouTube(f"https://youtube.com{results[0]['url_suffix']}")
            song_search = search_yt.streams.filter(only_audio = True).first()

            vc.play(discord.FFmpegPCMAudio(song_search.url, **FFMPEG_OPTIONS))
            search_embed = discord.Embed(title = f"Playing {search_yt.title}", color = 0xbbff00)
            search_embed.set_image(url = search_yt.thumbnail_url)

            await ctx.send(embed = search_embed)

    @commands.command()
    async def song(self, ctx: commands.Context, song_type: str = None):
        user = ctx.message.author
        voice_channel = user.voice.channel

        global voice_client
        voice_client = ctx.guild.voice_client

        channel = None

        if not voice_client in self.bot.voice_clients:
            channel = voice_channel
        else:
            channel = voice_client

        if voice_channel != None:
            if voice_client in self.bot.voice_clients:
                vc = channel
            else:
                vc = await channel.connect()
        
            if song_type == "pause":
                vc.pause()
                await ctx.send(embed = discord.Embed(title = "Paused song.", color = 0xff0000))
            elif song_type == "resume":
                vc.resume()
                await ctx.send(embed = discord.Embed(title = "Resumed song.", color = 0x00ff00))
            elif song_type == "stop":
                vc.stop()
                await ctx.send(embed = discord.Embed(title = "Stopped song.", color = 0xff0000))
            elif song_type == "kick":
                if ctx.author.guild_permissions.administrator:
                    await vc.disconnect()
                    await ctx.send(embed = discord.Embed(title = "Bot kicked from voice channel.", color = 0x00ff00))
                else:
                    await ctx.send(embed = discord.Embed(title = "You are not a staff member.", color = 0xff0000))
            else:
                command_embed = discord.Embed(title = "Commands:", description = f"""
                    {self.bot.command_prefix}song pause
                    {self.bot.command_prefix}song resume
                    {self.bot.command_prefix}song stop
                    {self.bot.command_prefix}song kick (staff only)
                """, color = 0xe86464)

                await ctx.send(embed = command_embed)

async def setup(bot):
    await bot.add_cog(Music(bot))