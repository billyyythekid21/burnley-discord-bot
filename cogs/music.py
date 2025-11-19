import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# FFmpeg and YoutubeDL options
FFMPEG_OPTIONS = {'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.current_title = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("music.py is ready!")

    @commands.hybrid_command(name="play", description="Plays the specified song in the current voice channel.", with_app_command=True)
    async def play(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("You're not connected to a voice channel!")

        # Connect to the voice channel if not already connected
        if not ctx.voice_client:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.move_to(voice_channel)

        # Search and add to queue
        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url = info['url']
                title = info['title']
                self.queue.append((url, title))
                await ctx.send(f"Added to queue: **{title}**")

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            self.current_title = title
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _: self.client.loop.create_task(self.play_next(ctx)))
            await ctx.send(f'Now playing: **{title}**')
        else:
            self.current_title = None
            await ctx.send("The music queue is currently empty!")

    @commands.hybrid_command(name="skip", description="Skips the current song.", with_app_command=True)
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("The current track has been skipped!")
        else:
            await ctx.send("No track is currently playing.")

    @commands.hybrid_command(name="pause", description="Pauses the current song.", with_app_command=True)
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused!")
        else:
            await ctx.send("No track is currently playing.")

    @commands.hybrid_command(name="resume", description="Resumes the current song.", with_app_command=True)
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed!")
        else:
            await ctx.send("The track is not paused.")

    @commands.hybrid_command(name="disconnect", description="Disconnects the bot from the voice channel.", with_app_command=True)
    async def disconnect(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            self.queue.clear()
            await ctx.send("Disconnected from the voice channel and cleared the queue.")
        else:
            await ctx.send("I'm not connected to a voice channel.")

async def setup(client):
    await client.add_cog(Music(client))